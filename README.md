# CAS-5A (FO-118) Satellite Images decoder
This is an CAS-5A (FO-118) Satellite Images decoder that works in conjunction with HS_soundmodem 

![1](https://github.com/Foxiks/CAS-5A-Images-Decoder/blob/main/img/1.jpg)

## Using
Before use, specify the port for KISS Server in your soudmodem settings. Settings->Devices->KISS Server port

![2](https://github.com/Foxiks/xw-3-images-decoder/blob/main/img/2.png)

After that run start.bat for Windows or:
```sh
TCP-CAS-5A_Decoder.exe -p (--port) 8100 -ip 127.0.0.1 -o out.png
```
or
```sh
python TCP-CAS-5A_Decoder.py -p (--port) 8100 -ip 127.0.0.1 -o out.png
```

Mode for sondmodem: FSK G3RUH 4800bd.

To request a photo, send a DTMF code to 2m band. Read more on pages 24-25 [here](https://ukamsat.files.wordpress.com/2022/12/camsat-cas-5a-amateur-radio-satellite-users-manual-v2.0.pdf)
