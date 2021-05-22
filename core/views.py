import hashlib
import pickle
import shutil
import os

import cv2
from PIL import ImageFont, ImageDraw, Image
from django.core.files.storage import FileSystemStorage
from django.http import StreamingHttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from core import models
# Create your views here.
from django.views.generic.edit import FormView
from core import faceRecognition
import face_recognition

class Home(FormView):
    def get(self, request):
        list_class = models.Class.objects.all()
        list_subject = models.Subject.objects.all()
        context = {'list_class': list_class, 'list_subject': list_subject}
        id_class = None
        id_subject = None
        list_student = None
        if 'class' in request.GET:
            id_class = request.GET['class']
        if 'subject' in request.GET:
            id_subject = request.GET['subject']
        if not id_class is None and not id_subject is None:
            list_student = models.Student.objects.filter(id_class__contains=id_class, id_subject__contains=id_subject)
        elif not id_class is None:
            list_student = models.Student.objects.filter(id_class__contains=id_class)
        elif not id_subject is None:
            list_student = models.Student.objects.filter(id_subject__contains=id_subject)
        else:
            list_student = models.Student.objects.all()
        if not list_student is None:
            context = {'list_class': list_class, 'list_subject': list_subject, 'list_student': list_student}
        return render(request, 'index.html', context)

    def face_detection(request, id_class, id_subject):
        contex = None
        if 'image_roll_up' in request.FILES:
            if 'date_roll_up' in request.POST:
                date_roll_up = request.POST['date_roll_up']
                dir_save_image = 'static/roll_up/' + id_class + '/' + id_subject + '/' + str(date_roll_up)
                if os.path.isdir(dir_save_image):
                    shutil.rmtree(dir_save_image)

            for file in request.FILES.getlist('image_roll_up'):
                fs = FileSystemStorage(dir_save_image)
                filename = fs.save(file.name, file)
                uploaded_file_url = fs.url(filename)

            if os.path.isdir(dir_save_image):
                list_image = []
                for item in os.listdir(dir_save_image):
                    dir_image = dir_save_image + '/' + item
                    list_image.append(dir_image)

            # resize image
            for item in list_image:
                img = cv2.imread(item, cv2.IMREAD_UNCHANGED)
                print('Original Dimensions : ', img.shape)
                MAX_WIDTH = 1080
                MAX_HEIGHT = 1080
                width = img.shape[1]
                height = img.shape[0]

                if width > height:
                    if width > MAX_WIDTH:
                        height *= MAX_WIDTH / width
                        width = MAX_WIDTH
                else:
                    if height > MAX_HEIGHT:
                        width *= MAX_HEIGHT / height
                        height = MAX_HEIGHT
                dim = (int(width), int(height))
                # resize image
                resized = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
                print('Resized Dimensions : ', resized.shape)
                cv2.imwrite(item, resized)
            # face recognition
            if not id_class is None and not id_subject is None:
                model_path = 'static/media/' + id_class + '/' + 'face_detection_' + id_class + '.clf'
                contex = faceRecognition.run(dir_save_image, model_path)
        else:
            print('No image')
        return contex

    def table(request):
        list_class = models.Class.objects.all()
        list_subject = models.Subject.objects.all()
        context = {'list_class': list_class, 'list_subject': list_subject}
        id_class = None
        id_subject = None
        list_student = None
        if 'class' in request.GET:
            id_class = request.GET['class']
        if 'subject' in request.GET:
            id_subject = request.GET['subject']
        if not id_class is None and not id_subject is None:
            list_student = models.Student.objects.filter(id_class__contains=id_class, id_subject__contains=id_subject)
        elif not id_class is None:
            list_student = models.Student.objects.filter(id_class__contains=id_class)
        elif not id_subject is None:
            list_student = models.Student.objects.filter(id_subject__contains=id_subject)
        else:
            list_student = models.Student.objects.all()
        if not list_student is None:
            context = {'list_class': list_class, 'list_subject': list_subject, 'list_student': list_student}
        return render(request, 'tables.html', context)

    def save_roll_up(date, id_class, id_subject, id_student):
        roll_up = models.Roll_up()
        roll_up.id_subject = id_subject
        roll_up.id_class = id_class
        roll_up.id_student = id_student
        roll_up.date = date
        roll_up.save()

    @csrf_exempt
    def edit_roll_up(request):
        date = request.POST['date_roll_up']
        id_class = request.POST['class']
        id_subject = request.POST['subject']
        models.Roll_up.objects.filter(date=date, id_class=id_class, id_subject=id_subject).delete()
        if 'list-roll-up' in request.POST:
            list = request.POST.getlist('list-roll-up')
            for item in list:
                Home.save_roll_up(date, id_class, id_subject, item)
        return redirect('/rollup/')

    @csrf_exempt
    def body_tables(request):
        list_class = models.Class.objects.all()
        list_subject = models.Subject.objects.all()
        context = {'list_class': list_class, 'list_subject': list_subject}
        id_class = None
        id_subject = None
        date = None
        list_student = None
        if 'class' in request.POST:
            id_class = request.POST['class']
        if 'subject' in request.POST:
            id_subject = request.POST['subject']
        if 'date_roll_up' in request.POST:
            date = request.POST['date_roll_up']
        if not id_class is None and not id_subject is None:
            list_student = models.Student.objects.filter(id_class__contains=id_class, id_subject__contains=id_subject)
        elif not id_class is None:
            list_student = models.Student.objects.filter(id_class__contains=id_class)
        elif not id_subject is None:
            list_student = models.Student.objects.filter(id_subject__contains=id_subject)
        else:
            list_student = models.Student.objects.all()
        if not list_student is None:
            context = {'list_class': list_class, 'list_subject': list_subject, 'list_student': list_student}

        list_roll_up = {}

        # du lieu khi diem danh
        result = Home.face_detection(request, id_class, id_subject)
        if not result is None:
            models.Roll_up.objects.filter(date=date, id_class=id_class, id_subject=id_subject).delete()
            for item in list_student:
                if item.msv in result['list_msv']:
                    Home.save_roll_up(date, id_class, id_subject, item.msv)

        # du lieu lich su diem danh
        list = []
        history_roll_up = models.Roll_up.objects.filter(date=date, id_class=id_class, id_subject=id_subject)
        if len(history_roll_up) != 0:
            for student in history_roll_up:
                list.append(student.id_student)
            for item in list_student:
                if item.msv in list:
                    list_roll_up[item.msv] = 1
                else:
                    list_roll_up[item.msv] = 0
            context['list_roll_up'] = list_roll_up
        dir = 'static/roll_up/' + id_class + '/' + id_subject + '/' + date
        if os.path.isdir(dir):
            list_image = []
            for item in os.listdir(dir):
                dir_image = dir + '/' + item
                list_image.append(dir_image)
            context['list_dir'] = list_image

        return render(request, 'body-table.html', context)

    def register(request):
        return render(request, 'register.html')

    @csrf_exempt
    def login(request):
        # request.session['login'] = 'true'
        # print(request.session['login'])
        # del request.session['login']
        email = None
        password = None
        if 'email' in request.POST:
            email = request.POST['email']
        if 'password' in request.POST:
            password = request.POST['password']
            password = hashlib.md5(password.encode()).hexdigest()
        if not email is None and not password is None:
            result = models.User.objects.filter(username=email, password = password)
            if result:
                request.session['login'] = 'true'
                return redirect('/')
            else:
                context = {'error': 'Wrong email or password. Please try again'}
                return render(request, 'login.html', context)
        return render(request, 'login.html')
    def logout(request):
        if 'login' in request.session:
            del request.session['login']
        return render(request, 'login.html')
    def addstudent(request):
        list_class = models.Class.objects.all()
        list_subject = models.Subject.objects.all()
        context = {'list_class': list_class, 'list_subject': list_subject}
        if 'id' in request.GET:
            id_student = request.GET['id']
            student = models.Student.objects.get(id=id_student)
            context['student'] = student

            dir = 'static/media/' + student.id_class + '/' + student.msv
            if os.path.isdir(dir):
                list_image = []
                for item in os.listdir(dir):
                    dir_image = dir + '/' + item
                    list_image.append(dir_image)
                if not list_image is None:
                    context['image_student'] = list_image
        return render(request, 'profile.html', context)

    def insert_student(request):
        name_user = request.POST['name_user'].strip()
        msv_user = request.POST['msv_user'].strip()
        birthday_user = request.POST['birthday_user']
        sex_user = request.POST['sex_user']
        address_user = request.POST['address_user'].strip()
        class_user = request.POST['class_user']
        # subject_user = request.POST['subject_user']
        subject_user = request.POST.getlist('subject_user')
        if 'btn-edit-student' in request.POST:
            id_student = request.POST['id_student']
            student = models.Student.objects.get(id=id_student)
            dir_image = 'static/media/' + student.id_class + '/' + student.msv
            student.name = name_user
            student.birthday = birthday_user
            student.msv = msv_user
            student.address = address_user
            student.id_class = class_user
            student.id_subject = subject_user
            student.sex = sex_user
            student.save()
            if 'image_user' in request.FILES:
                # neu thay doi avatar thi xoa avatar cu va them moi
                if os.path.isdir(dir_image):
                    shutil.rmtree(dir_image)
                for file in request.FILES.getlist('image_user'):
                    fs = FileSystemStorage('static/media/' + class_user + '/' + msv_user)
                    filename = fs.save(file.name, file)
                    uploaded_file_url = fs.url(filename)
                train_dir = 'static/media/' + class_user
                save_path = train_dir + '/' + 'face_detection_' + class_user +'.clf'
                faceRecognition.train(train_dir, model_save_path=save_path, n_neighbors=1)
            else:
                # neu khong thay doi avatar thi move anh tu folder cu sang folder moi
                if os.path.isdir(dir_image):
                    new_dir = 'static/media/' + class_user + '/' + msv_user
                    if new_dir != dir_image:
                        os.mkdir(new_dir)
                        for item in os.listdir(dir_image):
                            shutil.move(dir_image + '/' + item, new_dir + '/' + item)
                        shutil.rmtree(dir_image)
                        train_dir = 'static/media/' + class_user
                        save_path = train_dir + '/' + 'face_detection_' + class_user + '.clf'
                        faceRecognition.train(train_dir, model_save_path=save_path, n_neighbors=1)
            return redirect('/?success')
        else:
            if request.method == 'POST' and request.FILES['image_user']:
                student = models.Student()
                student.name = name_user
                student.birthday = birthday_user
                student.msv = msv_user
                student.address = address_user
                student.id_class = class_user
                student.id_subject = subject_user
                student.sex = sex_user
                student.save()
                for file in request.FILES.getlist('image_user'):
                    fs = FileSystemStorage('static/media/' + class_user + '/' + msv_user)
                    filename = fs.save(file.name, file)
                    uploaded_file_url = fs.url(filename)
                train_dir = 'static/media/' + class_user
                save_path = train_dir + '/' + 'face_detection_' + class_user + '.clf'
                faceRecognition.train(train_dir, model_save_path=save_path, n_neighbors=1)
            return redirect('/add/?success')

    def deleteStudent(request):
        if 'id' in request.GET:
            id_student = request.GET['id']
            student = models.Student.objects.get(id=id_student)
            dir = 'static/media/' + student.id_class + '/' + student.msv
            if os.path.isdir(dir):
                shutil.rmtree(dir)
            student.delete()
        return redirect('/')

    def manager(request):
        list_class = models.Class.objects.all()
        list_subject = models.Subject.objects.all()
        context = {'list_class': list_class, 'list_subject': list_subject}
        return render(request, 'manager.html', context)

    def manager_class(request):
        if 'class' in request.GET:
            class_name = request.GET['class']
            add_class = models.Class()
            add_class.name = class_name
            add_class.save()
        if 'subject' in request.GET:
            subject_name = request.GET['subject']
            add_subject = models.Subject()
            add_subject.name = subject_name
            add_subject.save()
        return redirect('/manager/')
    def manager_delete(request):
        if 'class' in request.GET:
            id_class = request.GET['class']
            models.Class.objects.get(id=id_class).delete()
        if 'subject' in request.GET:
            subject_name = request.GET['subject']
            models.Subject.objects.get(id=subject_name).delete()
        return redirect('/manager/')
    def manager_edit(request):
        if 'class' in request.GET:
            id_class = request.GET['class']
            name = request.GET['name']
            obj = models.Class.objects.get(id=id_class)
            obj.name = name
            obj.save()
        if 'subject' in request.GET:
            id_subject = request.GET['subject']
            name = request.GET['name']
            obj = models.Subject.objects.get(id=id_subject)
            obj.name = name
            obj.save()
        return redirect('/manager/')
    def report(request):
        list_class = models.Class.objects.all()
        list_subject = models.Subject.objects.all()
        contex = {'list_class': list_class, 'list_subject': list_subject}
        return render(request, 'report.html',contex)
    def body_report(request):
        id_class = None
        id_subject = None
        if 'class' in request.GET:
            id_class = request.GET['class']
        if 'subject' in request.GET:
            id_subject = request.GET['subject']
        data = models.Roll_up.objects.filter(id_class=id_class, id_subject=id_subject)
        list_student = models.Student.objects.filter(id_class=id_class, id_subject__contains=id_subject)
        list_class = models.Class.objects.all()
        list_subject = models.Subject.objects.all()
        list_date = []
        list_data = []
        summary = []
        for item in data:
            if not item.date in list_date:
                list_date.append(item.date)
        list_date.sort()
        for item in list_student:
            count = 0
            for date in list_date:
                result = models.Roll_up.objects.filter(date=date, id_student=item.msv, id_subject=id_subject, id_class=id_class)
                if not result:
                    obj = {'msv': item.msv, 'status': 0}
                    list_data.append(obj)
                    count += 1
                else:
                    obj = {'msv': item.msv, 'status': 1}
                    list_data.append(obj)
            smr = {'msv': item.msv, 'absent': count}
            summary.append(smr)
        contex = {'list_date': list_date, 'list_student': list_student, 'list_data': list_data, 'summary': summary,'list_class': list_class, 'list_subject': list_subject}
        return render(request, 'body-table-report.html',contex)


        # face recognition webcam

    def predict(X_face_locations, faces_encodings, knn_clf=None, model_path=None, distance_threshold=0.6):

        # Load a trained KNN model (if one was passed in)
        if knn_clf is None:
            with open(model_path, 'rb') as f:
                knn_clf = pickle.load(f)

        # If no faces are found in the image, return an empty result.
        if len(X_face_locations) == 0:
            return []

        # Use the KNN model to find the best matches for the test face
        closest_distances = knn_clf.kneighbors(faces_encodings, n_neighbors=1)
        are_matches = [closest_distances[0][i][0] <= distance_threshold for i in range(len(X_face_locations))]

        # Predict classes and remove classifications that aren't within the threshold
        return [(pred, loc) if rec else ("unknown", loc) for pred, loc, rec in
                zip(knn_clf.predict(faces_encodings), X_face_locations, are_matches)]

    def stream(request):
        video_capture = cv2.VideoCapture(0)
        process_this_frame = True
        list_student = []
        if 'class' in request.GET:
            id_class = request.GET['class']
        if 'subject' in request.GET:
            id_subject = request.GET['subject']
        if 'date_roll_up' in request.GET:
            date = request.GET['date_roll_up']
        while True:
            ret, frame = video_capture.read()
            if not ret:
                print("Error: failed to capture image")
                break
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            rgb_small_frame = small_frame[:, :, ::-1]
            if process_this_frame:
                # Find all the faces and face encodings in the current frame of video
                face_locations = face_recognition.face_locations(rgb_small_frame)
                face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
                model_path = 'static/media/' + id_class + '/' + 'face_detection_' + id_class + '.clf'
                predictions = Home.predict(faces_encodings=face_encodings, X_face_locations=face_locations,
                                      model_path=model_path)


            scale_percent = 200  # percent of original size
            width = int(frame.shape[1] * scale_percent / 100)
            height = int(frame.shape[0] * scale_percent / 100)

            if not predictions:
                small_frame = cv2.resize(frame, (0, 0), fx=3, fy=3)
                cv2.imwrite('face.jpg', small_frame)
            else:
                cv2.imwrite('face.jpg', frame)

            pil_image = Image.open('face.jpg').convert("RGB")
            draw = ImageDraw.Draw(pil_image)
            font = ImageFont.truetype("Roboto.ttf", 15)

            for name, (top, right, bottom, left) in predictions:
                # Scale back up face locations since the frame we detected in was scaled to 1/4 size
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4

                #get name from database and add student
                if name != 'unknown':
                    if not name in list_student:
                        list_student.append(name)
                        result = models.Roll_up.objects.filter(date=date, id_student=name, id_subject=id_subject,id_class=id_class)
                        if not result:
                                roll_up = models.Roll_up()
                                roll_up.id_class = id_class
                                roll_up.id_subject = id_subject
                                roll_up.id_student = name
                                roll_up.date = date
                                roll_up.save()
                    name_student = models.Student.objects.get(msv=name).name
                else:
                    name_student = name
                lable = name_student
                draw.rectangle(((left, top), (right, bottom)), outline=(0, 0, 255))
                draw.rectangle(((left, bottom - 20), (right, bottom)), fill=(0, 0, 255),outline=(0, 0, 255))
                draw.text((left + 6, bottom - 20), lable, font=font, fill=(255, 255, 255, 255))
                pil_image = pil_image.resize((width, height), Image.ANTIALIAS)
                pil_image.save("face.jpg")
                if name !='unknown':
                    dir = 'static/roll_up/' + id_class + '/' + id_subject + '/' + date
                    if not os.path.exists(dir):
                        os.makedirs(dir)
                    dir_save_image = dir + '/' + name + '.jpg'
                    if not os.path.isfile(dir_save_image):
                        pil_image.save(dir_save_image)

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + open('face.jpg', 'rb').read() + b'\r\n')


    def video_feed(request):
        return StreamingHttpResponse(Home.stream(request), content_type='multipart/x-mixed-replace; boundary=frame')




