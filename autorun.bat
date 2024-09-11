@echo off
cd /d "C:\Users\M Ortiz\Desktop\ITECH_Seikapp_monitor_master_cliente"
call venv\Scripts\activate
python run.py
echo %date% %time% Script executed >> tasks_log\script_log.txt




