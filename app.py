from flask import Flask, render_template, Response
from camera import VideoCamera
from video import VideoCamera1
import cv2
import mysql.connector
import csv

app = Flask(__name__) 

camera = cv2.VideoCapture(0)

def generate_frames():
    while True:
        success, frame = camera.read()
        
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            
@app.route('/video_cam')
def video_cam():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/base')
def base():
    return render_template('base.html')

@app.route('/base1')
def base1():
    return render_template('base1.html')

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n'+frame+b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
@app.route('/video_feed1')
def video_feed1():
    return Response(gen(VideoCamera1()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/Delete_Data')
def Delete_Data():
    try:
       connection = mysql.connector.connect(host='localhost',
                                            database='potholedata',
                                            user='root',
                                            password='')
       cursor = connection.cursor()
       Delete_all_rows = """truncate table pothole """
       cursor.execute(Delete_all_rows)
       connection.commit()
       print("All Record Deleted successfully ")

    except mysql.connector.Error as error:
       print("Failed to Delete all records from database pothole table: {}".format(error))
    finally:
       if connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection is closed")

    return 'Data Deleted successfully!'

@app.route('/export_data')
def export_data():
    # Connect to MySQL database
    connection = mysql.connector.connect(host='localhost',
                                         database='potholedata',
                                         user='root',
                                         password='')
    cursor = connection.cursor()

    # Execute SQL query to select data from table
    cursor.execute('SELECT * FROM pothole')

    # Create CSV file and write data to file
    with open('data.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([i[0] for i in cursor.description])
        writer.writerows(cursor.fetchall())

    # Close database connection
    cursor.close()
    connection.close()

    return 'Data exported successfully!'

if __name__ == '__main__':
    app.run(host="localhost",port="5000")
# if __name__ == '__main__':
#     app.run(debug=True)







