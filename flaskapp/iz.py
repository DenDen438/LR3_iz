print("Hello world")
from flask import Flask
app = Flask(__name__)
#декоратор для вывода страницы по умолчанию
@app.route("/")
def hello():
 return " <html><head></head> <body> Hello World! </body></html>"

from flask import render_template
#наша новая функция сайта

# модули работы с формами и полями в формах
from flask_wtf import FlaskForm,RecaptchaField
from wtforms import StringField, SubmitField, TextAreaField
# модули валидации полей формы
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileAllowed, FileRequired
# используем csrf токен, можете генерировать его сами
SECRET_KEY = 'secret'
app.config['SECRET_KEY'] = SECRET_KEY
# используем капчу и полученные секретные ключи с сайта google 
app.config['RECAPTCHA_USE_SSL'] = False
app.config['RECAPTCHA_PUBLIC_KEY'] = '6LdLblEbAAAAADc1wxPLbRn_qcFNcNT0F6Nf0V4R'
app.config['RECAPTCHA_PRIVATE_KEY'] = '6LdLblEbAAAAABe_9ETjzLx_8X-Y6WwDkI2lMIzg'
app.config['RECAPTCHA_OPTIONS'] = {'theme': 'white'}
# обязательно добавить для работы со стандартными шаблонами
from flask_bootstrap import Bootstrap
bootstrap = Bootstrap(app)
# создаем форму для загрузки файла
class NetForm(FlaskForm):
 # поле для введения строки, валидируется наличием данных
 # валидатор проверяет введение данных после нажатия кнопки submit
 # и указывает пользователю ввести данные если они не введены
 # или неверны
 cho = StringField('Введите значение, на которое нужно изменить яркость изображения (от 0 до 10)', validators = [DataRequired()])
 cho1 = StringField('Введите значение, на которое нужно изменить контраст изображения (от 0 до 10)', validators = [DataRequired()])
 # поле загрузки файла
 # здесь валидатор укажет ввести правильные файлы
 upload = FileField('Load image', validators=[
 FileRequired(),
 FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])
 # поле формы с capture
 recaptcha = RecaptchaField()
 #кнопка submit, для пользователя отображена как send
 submit = SubmitField('send')
# функция обработки запросов на адрес 127.0.0.1:5000/net
# модуль проверки и преобразование имени файла
# для устранения в имени символов типа / и т.д.
from werkzeug.utils import secure_filename
import os

import numpy as np
from PIL import Image, ImageEnhance
import matplotlib.pyplot as plt
import seaborn as sns

## функция для обработки изображения 
def draw(filename,cho, cho1):
 ##открываем изображение 
 print(filename)
 image= Image.open(filename)
 x = image.size[0] #Определяем ширину. 
 y = image.size[1] #Определяем высоту. 	
 cho=int(cho)
 cho1=int(cho1)
 
 ##делаем график
 fig = plt.figure(figsize=(6, 4))
 ax = fig.add_subplot()
 data = np.random.randint(0, 255, (100, 100))
 ax.imshow(image, cmap='plasma')
 b = ax.pcolormesh(data, edgecolors='black', cmap='plasma')
 fig.colorbar(orientation='horizontal', b, ax=ax)
 sns.displot(data)
 plt.savefig("./static/newgr.png")
 plt.close()


##меняем яркость
 image1=ImageEnhance.Brightness(image).enhance(cho)	   
 image1.save("./static/img1.png")
 image2=ImageEnhance.Contrast(image).enhance(cho1)	  
 image2.save("./static/img2.png")
 
 ax.imshow(image1, cmap='plasma')
 b = ax.pcolormesh(data, edgecolors='black', cmap='plasma')
 fig.colorbar(orientation='horizontal', b, ax=ax)
 plt.savefig("./static/newgr1.png")
 plt.close()

 ax.imshow(image2, cmap='plasma')
 b = ax.pcolormesh(data, edgecolors='black', cmap='plasma')
 fig.colorbar(orientation='horizontal', b, ax=ax)
 plt.savefig("./static/newgr2.png")
 plt.close()
 
 output_filename = filename
 image.save(output_filename)
 
 return output_filename



# метод обработки запроса GET и POST от клиента
@app.route("/net",methods=['GET', 'POST'])
def net():
 # создаем объект формы
 form = NetForm()
 # обнуляем переменные передаваемые в форму
 filename=None
 newfilename=None
 grname=None
 # проверяем нажатие сабмит и валидацию введенных данных
 if form.validate_on_submit():
  # файлы с изображениями читаются из каталога static
  filename = os.path.join('./static', secure_filename(form.upload.data.filename))
  ch=form.cho.data
  ch1=form.cho1.data
 
  form.upload.data.save(filename)
  newfilename = draw(filename,ch, ch1)
 # передаем форму в шаблон, так же передаем имя файла и результат работы нейронной
 # сети если был нажат сабмит, либо передадим falsy значения
 
 return render_template('net.html',form=form,image_name=newfilename,gr_name=grname)


if __name__ == "__main__":
 app.run(host='127.0.0.1',port=5000)
