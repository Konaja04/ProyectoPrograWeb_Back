mensaje_html = """
<html>
<head>
    <style>
        body {{
            background-color: #FFD6C;
            font-family: 'Arial', sans-serif;
            color: #333333;
            margin: 0;
            padding: 0;
        }}
        .container {{
            width: 100%;
            max-width: 600px;
            margin: 20px auto;
            padding: 20px;
            background-color: #fff;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }}
        .header {{
            background-color: #FF6A00;
            padding: 10px 20px;
            text-align: center;
        }}
        .header img {{
            width: 150px;
        }}
        .content {{
            padding: 20px;
            text-align: left;
        }}
        .footer {{
            margin-top: 20px;
            text-align: center;
            padding: 10px;
            font-size: 12px;
            background-color: #f2f2f2;
        }}
        .button {{
            display: inline-block;
            padding: 10px 20px;
            margin: 10px auto;
            background-color: #FF6A00;
            color: #ffffff;
            text-decoration: none;
            border-radius: 5px;
        }}
        .qr-code {{
            margin: 20px auto;
            display: block;
            width: 180px;
        }}
        .receipt {{
            margin: 20px 0;
            padding: 20px;
            background-color: #f9f9f9;
            border: 1px solid #ddd;
        }}
        .receipt h2 {{
            margin-top: 0;
        }}
        .receipt-item {{
            margin-bottom: 10px;
        }}
        .receipt-item span {{
            font-weight: bold;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <img src="https://admision.ulima.edu.pe/wp-content/uploads/2023/03/UdeLIMA_Logos-01-1.png" alt="Logo de la Universidad de Lima">
        </div>
        <div class="content">
            <div class="receipt">
                <h2>Confirmación de Reserva</h2>
                <div class="receipt-item">
                    <span>Nombre:</span> {nombre}
                </div>
                <div class="receipt-item">
                    <span>Apellido:</span> {apellido}
                </div>
                <div class="receipt-item">
                    <span>Película:</span> "{peli}"
                </div>
                <div class="receipt-item">
                    <span>Sala:</span> {sala}
                </div>
                <div class="receipt-item">
                    <span>Cantidad de Personas:</span> {cantidad}
                </div>
                <div class="receipt-item">
                    <img src="https://t3.gstatic.com/licensed-image?q=tbn:ANd9GcSh-wrQu254qFaRcoYktJ5QmUhmuUedlbeMaQeaozAVD4lh4ICsGdBNubZ8UlMvWjKC" alt="Código QR" class="qr-code">
                </div>
                <p>No olvides presentar este código en la entrada del cine.</p>
            </div>
            <p>Disfruta la función!</p>
            <a href="https://localhost:3000/reservas" class="button">Ver detalles de la reserva</a>
        </div>
        <div class="footer">
            Salas de Cine Ulima &copy; 2024
        </div>
    </div>
</body>
</html>
"""

def devolver_mensaje(data):
    nombre = data['nombre']
    apellido = data['apellido']
    cantidad = data['cantidad']
    sala = data['sala']
    peli = data['peli']  
    return mensaje_html.format(nombre=nombre, apellido=apellido, cantidad=cantidad, sala=sala, peli=peli)
