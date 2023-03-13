# PlateNumberWebApi

This is a Flask Web Api that will help the user to detect the number plate position and read the number plate using tesseract-ocr ,
the machine learning modul was created using YoloV5 .
Also this api will be part of an Android application created using React-Native

## Used Technologies 
***the app was made using:*** Python,Flask ,tesseract ,YoloV5 ,Docker,elephantsql,postgresql

## Environment Variables

To run this project locally , you will need to add the following environment variables to your .env file

`DATABASE_URL` this should include the link for your **elephantsql** instance

also you will need to install the packages inside  `requirements.txt` using:

`pip install -r requirements.txt`

and you might also need to install tesseract-ocr it self .

## API Reference

#### How to use

to view the schema: https://plate-number-flask-api.onrender.com/swagger-ui

```http
  POST /register
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `username` | `string` | **Required**. |
| `email` | `string` | **Required**. |
| `password` | `string` | **Required**. |

and to after that you can login at 

```http
  POST /login   
```
| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `email` | `string` | **Required**. |
| `password` | `string` | **Required**. |

this will give you the access token that you will use to for the /api/object_detection_text

```http
  POST /api/object_detection_text   
```
| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `image_name` | `File` | **Required**. |

you need to chose form-data body format if you are using Postman to upload the image .












