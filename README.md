## Certo

sudo docker-compose up --build

sudo docker exec -it certo_web_1 /bin/bash


to add data storage volume follow https://creodias.eu/-/how-to-attach-a-volume-to-vm-2-tb-linux-?inheritRedirect=true&redirect=%2Ffaq-data-volume

When running cylc you need to edit the global.rc file and change https to http. 
/opt/cylc-flow-7.9.3/etc/global.rc

Run with "cylc cat-log -o intro hello.1" with hello being the process name and intro being the suite/folder