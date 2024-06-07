from flask import Flask, render_template, request, send_file
from pytube import YouTube
from io import BytesIO

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        format = request.form['format']
        resolution = request.form['resolution']

        try:
            yt = YouTube(url)
            streams = yt.streams.filter(file_extension=format, res=resolution).all()

            if streams:
                stream = streams[0]
                video_buffer = BytesIO()
                stream.stream_to_buffer(video_buffer)
                video_buffer.seek(0)
                return send_file(video_buffer, as_attachment=True, download_name=f"{yt.title}.{format}")
            else:
                return "No stream found with the specified resolution and format."
        except Exception as e:
            return str(e)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)