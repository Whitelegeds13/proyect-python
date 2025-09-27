from django.shortcuts import render

def galeria(request):
    # Define las imágenes que quieres mostrar en el carrusel
    imagenes = [
        'app/img/galeria1.jpg',  # Asegúrate de tener estas imágenes en tu carpeta static
        'app/img/galeria2.jpg',
        'app/img/galeria3.jpg',
        'app/img/galeria4.jpg'
    ]
    return render(request, 'app/galeria.html', {'imagenes': imagenes})