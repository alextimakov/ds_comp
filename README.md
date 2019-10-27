# Компетенции для Data Science команды 

### Для работы над проектом:

1. Склонируйте проект в нужную папку: 

`git clone https://github.com/alextimakov/ds_comp.git`

2. Распакуйте проект и создайте виртуальное окружение в нём:

```
cd ./ds_comp
python3 -m venv venv
```

3. Зайдите в созданное окружение и установите pip-tools:

```
source venv/bin/activate
pip install pip-tools
```

4. Установите в окружение необходимые зависимости:

`pip-sync`


### Возникающие ошибки

#### Ошибка pip
- При установке пакетов через pip возникает ошибка типа: 
`pip install fails with “connection error: [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed (_ssl.c:598)”`. 

- Решаем с помощью установки в обход сертификатов:
`pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org <package_name>`

- Работает и в случае с прямой установкой через pip, так и через `pip-sync`


### Правила работы над проектом
1. Все адреса, логины и пароли тянутся из `config.py`. 
Он включен в `.gitconfig` не просто так, просьба НЕ ПУШИТЬ его в репозиторий.
Темплейт конфигурации - в `config_examply.py`.

2. Версионирование проекта - по [semver](https://semver.org/).
Позднее настроим автоматическую накатку версий. 

3. Не забываем о правилах работы с удалённым репозиторием:
    - Обязательно - делать `git pull` перед началом работ и мержить конфликты перед каждым пушем
    - Если возникает мёрж конфликт, то не забываем пообщаться с автором конфликтующей версии и только после этого убивать его кусок кода