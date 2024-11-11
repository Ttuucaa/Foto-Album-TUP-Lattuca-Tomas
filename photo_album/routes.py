from flask import Blueprint, render_template, redirect, url_for, request, flash
from models import db, Photo
from forms import PhotoForm
import os

photo_bp = Blueprint('photos', __name__)

@photo_bp.route('/')
def index():
    photos = Photo.query.all()
    return render_template('index.html', photos=photos)

@photo_bp.route('/add', methods=['GET', 'POST'])
def add_photo():
    form = PhotoForm()
    if form.validate_on_submit():
        image_file = form.image.data
        
        # Verifica si la subcarpeta 'static/images/' existe, y si no, la crea
        images_folder = os.path.join(os.getcwd(), 'static', 'images')
        if not os.path.exists(images_folder):
            os.makedirs(images_folder)
        
        # Construye la ruta completa para guardar la imagen
        image_path = os.path.join(images_folder, image_file.filename)
        image_file.save(image_path)
        
        # Guarda la ruta relativa en la base de datos
        new_photo = Photo(
            title=form.title.data,
            description=form.description.data,
            image=f'static/images/{image_file.filename}'
        )
        db.session.add(new_photo)
        db.session.commit()
        flash('Photo added successfully!')
        return redirect(url_for('photos.index'))
    return render_template('photo_form.html', form=form)

@photo_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_photo(id):
    photo = Photo.query.get_or_404(id)
    form = PhotoForm(obj=photo)
    if form.validate_on_submit():
        photo.title = form.title.data
        photo.description = form.description.data
        db.session.commit()
        flash('Photo updated successfully!')
        return redirect(url_for('photos.index'))
    return render_template('photo_form.html', form=form)

@photo_bp.route('/delete/<int:id>', methods=['POST'])
def delete_photo(id):
    photo = Photo.query.get_or_404(id)
    db.session.delete(photo)
    db.session.commit()
    flash('Photo deleted successfully!')
    return redirect(url_for('photos.index'))
