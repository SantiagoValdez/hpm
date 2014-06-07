#!/bin/bash
cp -R ./ /home/santiago/work/hpm/
cd /home/santiago/work/hpm/
sh ./inicializar_bd.sh
chmod 777 ./hpm/wsgi.py
chmod -R 777 ./media/