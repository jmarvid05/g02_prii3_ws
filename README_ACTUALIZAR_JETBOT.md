## Actualizar el repositorio en el JetBot

Una vez conectado al JetBot, ejecutar:

```bash
cd ~

rm -rf ~/g02_prii3_ws

git config --global user.name "jmarvid05"
git config --global user.email "jmarvid@upv.edu.es"

git clone -b main https://github.com/jmarvid05/g02_prii3_ws.git

cd ~/g02_prii3_ws

git branch
git status
```

Comprobar también la configuración de Git:

```bash
git config --global --list
```

Debe aparecer:

```text
user.name=jmarvid05
user.email=jmarvid@upv.edu.es
```

Y el repositorio debe quedar en:

```text
* main
```

con:

```text
nothing to commit, working tree clean
```

