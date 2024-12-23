
## Запуск
**Запуск плохого bad_Dockerfile**:
```bash
docker build -t jupyterhub-bad -f bad_Dockerfile .
docker run -d -p 8000:8000 -v jupyterhub_data:/data --name jupyterhub-bad jupyterhub-bad
 ```
 **Запуск исправленного good_Dockerfile**:

 ```bash
docker build -t jupyterhub-good -f Dockerfile.good .
docker run -d \
    -p 8000:8000 \
    -v jupyterhub_data:/home/jupyter_user/data \
    --name jupyterhub \
    jupyterhub-good
```
## Плохие практики в Bad Dockerfile и их исправление
1. **Использование неверсионированных пакетов**
   - Bad: `apt install -y python3-dev git`
   - OK: `python3-dev=3.9.2-3 git=1:2.30.2-1`
   - Why: Без фиксации версий невозможно гарантировать воспроизводимость сборки!

2. **Отсутствие очистки кэша apt**
   - Bad: не удаляем кэша после установки
   - OK: `rm -rf /var/lib/apt/lists/*`
   - Why: Увеличивает размер образа

3. **Запуск от root** !!!
   - Bad: Отсутствие создания пользователя
   - OK: Создание и использование `jupyter_user`
   - Why: Контейнер - это просто еще один процесс, запущенный с правами root на ядре хоста, получается, мы даем root-права нашему приложению не только внутри контейнера, но и на хосте.

4. **Неправильное объявление volumes**
   - Плохо: Простое `VOLUME /data`
   - Хорошо: `VOLUME ["/home/jupyter_user/data"]`
   - Причина: Отсутствие четкой структуры и прав доступа

## Плохие практики использования контейнеров

1. **Хранение важных данных внутри контейнера**
   - Контейнеры должны быть stateless
   - Все важные данные должны храниться в volumes

2. **Запуск множества сервисов в одном контейнере**
   - Каждый контейнер должен выполнять одну функцию
   - Усложняет масштабирование и мониторинг
   - Лучше использовать docker-compose для связанных сервисов

## Когда НЕ стоит использовать контейнеры

1. **Приложения с требованиями к производительности**
   - Контейнеризация добавляет overhead
   - Критично для систем реального времени
   - Примеры: HFT-трейдинг, обработка видео в реальном времени

2.  **Хранение важных данных внутри контейнера**
   - Контейнеры должны быть stateless
   - Все важные данные должны храниться в volumes

3. **Монолиты**
   - Большой монолит как правило имеет сложную структуру зависимостей, что делает сборку невероятно медленной, отладку – сложной, использование – неудобным.


