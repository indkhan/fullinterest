(* 1. Update the operation types - add division *)
type op = Add | Mul | Sub | Div | Leq | Eq | Geq | And | Or

(* 2. Keep the existing type system *)
type ty = Int | Bool | Fun of ty * ty

(* 3. Update the expression type to include lambda, function application, and recursive let *)
type exp =
 | Icon of int
 | Bcon of bool
 | Var of string
 | If of exp * exp * exp
 | Oapp of exp * op * exp
 | Let of string * exp * exp
 | Lambda of string * ty * exp
 | App of exp * exp
 | LetRec of string * string * ty * ty * exp * exp

(* examples *)
let rec map f l = match l with
 | [] -> []
 | x :: l -> (f x) :: map f l
let examples = [
  Oapp (Icon 2, Leq, Icon 3); (* 2 <= 3 *)
  Oapp (Var "x", Leq, Icon 3); (* x <= 3 *)
  If (Icon 0, Icon 0, Var "x"); (* if 0 then 0 else x *)
  If (Oapp (Var "x", Leq, Icon 0), Icon 0, Var "x");
  (* if x <= 0 then 0 else x *)
  Let ("x", Icon 1, Oapp (Var "x", Add, Icon 1));
  (* let x = 1 in x+1 *)
  Oapp (Var "x", Eq, Var "y"); (* x = y *)
  Oapp (Icon 5, Geq, Icon 3); (* 5 >= 3 *)
  Oapp (Bcon true, And, Bcon false); (* true && false *)
  Oapp (Bcon true, Or, Bcon false); (* true || false *)
  Oapp (Icon 5, Eq, Icon 5); (* 5 = 5 *)
  Oapp (Icon 6, Div, Icon 2); (* 6 / 2 *)
  Lambda ("x", Int, Oapp (Var "x", Add, Icon 1)); (* fun (x: int) -> x + 1 *)
  App (Lambda ("x", Int, Oapp (Var "x", Add, Icon 1)), Icon 2); (* (fun (x: int) -> x + 1) 2 *)
  LetRec ("f", "x", Int, Int, Oapp (Var "x", Add, Icon 1), App (Var "f", Icon 2)); (* let rec f (x: int): int = x + 1 in f 2 *)
]

(* environments *)
let rec lookup k l = match l with
 | [] -> None
 | (k', v) :: l -> if k = k' then Some v else lookup k l
let rec update k v l = match l with
 | [] -> [(k, v)]
 | (k', v') :: l -> if k = k' then (k, v) :: l
                    else (k', v') :: update k v l
type 'a env = (string * 'a) list

(* type checking *)
type tenv = ty env

let rec check_ty (tyenv: tenv) (e: exp) = match e with
 | Icon _ -> Some Int
 | Bcon _ -> Some Bool
 | Var x -> lookup x tyenv
 | If (e1, e2, e3) -> let t1 = check_ty tyenv e1 in
                      let t2 = check_ty tyenv e2 in
                      let t3 = check_ty tyenv e3 in
                      (match t1, t2, t3 with
                      | (Some Bool, Some x, Some y) ->
                        if x = y then Some x else None
                      | _ -> None)
 | Let (x, e1, e2) -> let t1 = check_ty tyenv e1 in
                      (match t1 with
                      | None -> None
                      | Some tx -> let tyenv' = update x tx tyenv in check_ty tyenv' e2)
 | Oapp (e1, o, e2) -> let t1 = check_ty tyenv e1 in
                       let t2 = check_ty tyenv e2 in
                       (match t1, o, t2 with
                        | (Some Int, Add, Some Int) -> Some Int
                        | (Some Int, Mul, Some Int) -> Some Int
                        | (Some Int, Sub, Some Int) -> Some Int
                        | (Some Int, Div, Some Int) -> Some Int (* Add division operator typing *)
                        | (Some Int, Leq, Some Int) -> Some Bool
                        (* Add equality operator typing *)
                        | (Some Int, Eq, Some Int) -> Some Bool
                        | (Some Bool, Eq, Some Bool) -> Some Bool
                        (* Add greater than or equal operator typing *)
                        | (Some Int, Geq, Some Int) -> Some Bool
                        (* Add logical operators typing *)
                        | (Some Bool, And, Some Bool) -> Some Bool
                        | (Some Bool, Or, Some Bool) -> Some Bool
                        | _ -> None)
 | Lambda (x, t1, e) -> 
     let tyenv' = update x t1 tyenv in
     (match check_ty tyenv' e with
      | Some t2 -> Some (Fun (t1, t2))
      | None -> None)
 | App (e1, e2) -> 
     (match check_ty tyenv e1, check_ty tyenv e2 with
      | Some (Fun (t1, t2)), Some t3 when t1 = t3 -> Some t2
      | _ -> None)
 | LetRec (f, x, t1, t2, e1, e2) ->
     let tyenv' = update f (Fun (t1, t2)) tyenv in
     let tyenv'' = update x t1 tyenv' in
     (match check_ty tyenv'' e1 with
      | Some t3 when t3 = t2 -> check_ty tyenv' e2
      | _ -> None)
  
(* evaluator *)
type va = Ival of int | Bval of bool
  | Cl of string * exp * venv
  | Cr of string * string * exp * venv
and venv = va env

let rec eval (env: venv) (e: exp) : va = match e with
  | Icon c -> Ival c
  | Bcon b -> Bval b
  | Var x -> (match lookup x env with Some v -> v
             | None -> failwith "Missing value")
  | If (e1, e2, e3) -> (match eval env e1 with
                        | Bval true -> eval env e2
                        | Bval false -> eval env e3
                        | _ -> failwith "Type not correct")
  | Let (x, e1, e2) -> (let vx = eval env e1 in
                        let env' = update x vx env in
                        eval env' e2)
  | Oapp (e1, o, e2) -> let v1 = eval env e1 in
                       let v2 = eval env e2 in
                       (match o, v1, v2 with
                         | Add, Ival x, Ival y -> Ival (x+y)
                         | Mul, Ival x, Ival y -> Ival (x*y)
                         | Sub, Ival x, Ival y -> Ival (x-y)
                         | Div, Ival x, Ival y -> 
                           if y = 0 then failwith "Division by zero"
                           else Ival (x/y) (* Add division operator evaluation *)
                         | Leq, Ival x, Ival y -> Bval (x<=y)
                         (* Add equality operator evaluation *)
                         | Eq, Ival x, Ival y -> Bval (x=y)
                         | Eq, Bval x, Bval y -> Bval (x=y)
                         (* Add greater than or equal operator evaluation *)
                         | Geq, Ival x, Ival y -> Bval (x>=y)
                         (* Add logical operators evaluation *)
                         | And, Bval x, Bval y -> Bval (x && y)
                         | Or, Bval x, Bval y -> Bval (x || y)
                         | _ -> failwith "Illegal value")
  | Lambda (x, t, e) -> Cl (x, e, env)
  | App (e1, e2) -> 
      (match eval env e1 with
       | Cl (x, e, env') -> 
           let v = eval env e2 in
           let env'' = update x v env' in
           eval env'' e
       | Cr (f, x, e, env') ->
           let v = eval env e2 in
           let env'' = update x v env' in
           let rec_env = update f (Cr (f, x, e, env')) env'' in
           eval rec_env e
       | _ -> failwith "Application of non-function")
  | LetRec (f, x, t1, t2, e1, e2) ->
      let env' = update f (Cr (f, x, e1, env)) env in
      eval env' e2

let run tenv venv e =
  match check_ty tenv e with
    | Some _ -> Some (eval venv e)
    | _ -> None
    
(* helper functions *)
let rec rev xs =
  let rec rev' xs a = match xs with
    | [] -> a
    | x::xr -> rev' xr (x::a)
  in rev' xs []

let rec map f l = match l with
 | [] -> []
 | x :: l -> (f x) :: map f l

(* split string into a list of characters *)
let explode s =
  let rec explode' i l =
    if i = 0 then l 
             else explode' (i - 1) (String.get s (i - 1) :: l) in
  explode' (String.length s) []
  
(* construct string from a list of characters *)
let implode cs =
  let rec implode' cs s = match cs with
    | [] -> s
    | c::cr -> implode' cr (s ^ (String.make 1 c))
  in implode' cs ""

(* Example for match-when *)
let sign x = match x with
  | x when x > 0 ->  1
  | x when x = 0 ->  0
  | x            -> -1
      
(* language tokens (lexer output) *)
type const = BCON of bool | ICON of int
type token = LP | RP | EQ | COL | ARR | ADD | SUB | MUL | DIV | LEQ | GEQ | EQEQ | AND | OR
           | IF | THEN | ELSE | LAM | LET | IN | REC | FUN
           | CON of const | VAR of string | BOOL | INT
                     
(* Mini-OCaml lexer *)
let lex s : token list =
  let is_digit c = '0' <= c && c <= '9' in
  let is_lower c = 'a' <= c && c <= 'z' in
  let is_upper c = 'A' <= c && c <= 'Z' in
  let is_whitespace c = match c with ' ' | '\t' | '\n' | '\r' -> true 
                                   | _ -> false in
  let digit_val c = Char.code c - Char.code '0' in
  let rec lex' cs acc = match cs with
    | [] -> rev acc
    | '('::cr -> lex' cr (LP::acc)
    | ')'::cr -> lex' cr (RP::acc)
    | '='::'='::cr -> lex' cr (EQEQ::acc)  (* Equality operator *)
    | '='::cr -> lex' cr (EQ::acc)
    | ':'::cr -> lex' cr (COL::acc)
    | '-'::'>'::cr -> lex' cr (ARR::acc)
    | '+'::cr -> lex' cr (ADD::acc)
    | '-'::cr -> lex' cr (SUB::acc)
    | '*'::cr -> lex' cr (MUL::acc)
    | '/'::cr -> lex' cr (DIV::acc)        (* Division operator *)
    | '<'::'='::cr -> lex' cr (LEQ::acc)
    | '>'::'='::cr -> lex' cr (GEQ::acc)  (* Greater than or equal operator *)
    | '&'::'&'::cr -> lex' cr (AND::acc)  (* Logical AND operator *)
    | '|'::'|'::cr -> lex' cr (OR::acc)   (* Logical OR operator *)
    | c::cr when is_digit c -> lex_num (c::cr) acc 0
    | c::cr when is_lower c -> lex_id (c::cr) acc []
    | c::cr when is_whitespace c -> lex' cr acc
    | _ -> failwith "lex: illegal character"
  and lex_num cs acc n = match cs with (* lex a numeric constant *)
    | c::cr when is_digit c -> lex_num cr acc (n * 10 + digit_val c)
    | _ -> lex' cs (CON(ICON(n))::acc)
  and lex_id cs acc id = match cs with (* lex an identifier or keyword *)
    | c::cr when is_lower c -> lex_id cr acc (c::id)
    | c::cr when is_upper c -> lex_id cr acc (c::id)
    | c::cr when is_digit c -> lex_id cr acc (c::id)
    | '_'::cr -> lex_id cr acc ('_'::id)
    | '\''::cr -> lex_id cr acc ('\''::id)
    | _ -> lex_id' cs (implode (rev id)) acc
  and lex_id' cs id acc = match id with (* lex keywords *)
    | "true" -> lex' cs (CON(BCON(true))::acc)
    | "false" -> lex' cs (CON(BCON(false))::acc)
    | "if" -> lex' cs (IF::acc)
    | "then" -> lex' cs (THEN::acc)
    | "else" -> lex' cs (ELSE::acc)
    | "fun" -> lex' cs (FUN::acc)
    | "let" -> lex' cs (LET::acc)
    | "rec" -> lex' cs (REC::acc)
    | "in" -> lex' cs (IN::acc)
    | "and" -> lex' cs (AND::acc)  (* 'and' keyword - alternative to && *)
    | "or" -> lex' cs (OR::acc)    (* 'or' keyword - alternative to || *)
    | "int" -> lex' cs (INT::acc)  (* Add support for 'int' type keyword *)
    | "bool" -> lex' cs (BOOL::acc) (* Add support for 'bool' type keyword *)
    | _ -> lex' cs (VAR(id)::acc)
  in lex' (explode s) []

(* Mini-OCaml parser *)
exception ExpectedVar of token list
exception ExpectedToken of token * token list
exception ExpectedType of token list

(* check if next token in ts is identifier *)
let expect_var ts = match ts with
  | VAR s :: ts -> s, ts
  | _ -> raise (ExpectedVar ts)

(* check if next token in ts is t *)
let expect t ts = match ts with
  | t' :: ts when t = t' -> ts
  | _ -> raise (ExpectedToken (t, ts))

(* Parse a type *)
let rec parse_type ts = match ts with
  | INT :: tr -> Int, tr
  | BOOL :: tr -> Bool, tr
  | LP :: tr -> 
      let t1, tr = parse_type tr in
      let tr = expect ARR tr in
      let t2, tr = parse_type tr in
      let tr = expect RP tr in
      Fun (t1, t2), tr
  | _ -> raise (ExpectedType ts)

let parse_exp ts =
  let rec parse_simple ts = match ts with 
    (* parse high-level structures using recursive descent *)
    | VAR s :: tr -> Var s, tr
    | CON (ICON c) :: tr -> Icon c, tr
    | CON (BCON c) :: tr -> Bcon c, tr
    | LP :: tr -> let e, tr = parse_binary tr in  (* parse parentheses: (e1) *)
                  let    tr = expect RP tr in
                  e, tr
    | IF :: tr -> let e1, tr = parse_binary tr in (* parse conditional: if e1 then e2 else e3 *)
                  let     tr = expect THEN tr in
                  let e2, tr = parse_binary tr in
                  let     tr = expect ELSE tr in
                  let e3, tr = parse_binary tr in
                  If (e1, e2, e3), tr
    | LET :: REC :: tr -> (* parse recursive declaration: let rec f (x: t1): t2 = e1 in e2 *)
        let f, tr = expect_var tr in
        let tr = expect LP tr in
        let x, tr = expect_var tr in
        let tr = expect COL tr in
        let t1, tr = parse_type tr in
        let tr = expect RP tr in
        let tr = expect COL tr in
        let t2, tr = parse_type tr in
        let tr = expect EQ tr in
        let e1, tr = parse_binary tr in
        let tr = expect IN tr in
        let e2, tr = parse_binary tr in
        LetRec (f, x, t1, t2, e1, e2), tr
    | LET:: tr -> let  x, tr = expect_var  tr in (* parse local declaration: let X = e1 in e2 *)
                  let     tr = expect EQ   tr in
                  let e1, tr = parse_binary tr in
                  let     tr = expect IN   tr in
                  let e2, tr = parse_binary tr in
                  Let (x, e1, e2), tr
    | FUN :: tr -> (* parse lambda: fun (x: t) -> e *)
        let tr = expect LP tr in
        let x, tr = expect_var tr in
        let tr = expect COL tr in
        let t, tr = parse_type tr in
        let tr = expect RP tr in
        let tr = expect ARR tr in
        let e, tr = parse_binary tr in
        Lambda (x, t, e), tr
    | _ -> failwith "parse: illegal tokens"
  and parse_binary ts = 
    (* parse binary (infix) operators using operator precedence parsing *)
    let rec parse_prec p (l, ts) = match parse_op ts with
      | None -> (* Try to parse as function application if not an operator *)
          (match ts with
          | LP :: _ | VAR _ :: _ | CON _ :: _ ->
              let r, ts' = parse_simple ts in
              parse_prec p (App (l, r), ts')
          | _ -> l, ts)
      | Some (op, lp, rp, ts') -> 
          if lp < p then (l, ts)
                    else let r, ts = parse_prec rp (parse_simple ts')
                         in parse_prec p (op l r, ts)
    in parse_prec 0 (parse_simple ts)
  and parse_op ts =
    let create_oapp op l r = Oapp (l, op, r) in 
    match ts with
      | LEQ :: tr -> Some (create_oapp Leq, 1, 1, tr)
      | GEQ :: tr -> Some (create_oapp Geq, 1, 1, tr)
      | EQEQ :: tr -> Some (create_oapp Eq, 1, 1, tr)
      | AND :: tr -> Some (create_oapp And, 0, 0, tr)  (* Lowest precedence *)
      | OR :: tr -> Some (create_oapp Or, 0, 0, tr)    (* Lowest precedence *)
      | ADD :: tr -> Some (create_oapp Add, 2, 3, tr)
      | SUB :: tr -> Some (create_oapp Sub, 2, 3, tr)
      | MUL :: tr -> Some (create_oapp Mul, 4, 5, tr)
      | DIV :: tr -> Some (create_oapp Div, 4, 5, tr)  (* Same precedence as multiplication *)
      | _         -> None
  in match parse_binary ts with 
    (* check that all tokens were eaten by parser*)
    | t, [] -> t
    | _ -> failwith "parse: junk at end"
 
let doit exp = 
  let a = check_ty [] (parse_exp (lex exp)) in 
  match a with
  | Some _ -> eval [] (parse_exp (lex exp))
  | None -> invalid_arg "Type error"
;;


(* Run some examples *)
let test_div_result = doit "6 / 2"
let test_lambda_app = doit "(fun (x: int) -> x + 1) 2"
let test_factorial = doit "let rec f (x: int): int = if x <= 0 then 1 else x * f (x - 1) in f 5"
