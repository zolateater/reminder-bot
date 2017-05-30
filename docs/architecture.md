# Архитектура #

Приложение использует 2 очереди rabbitmq:
- `telegram_messages` - для обработки входящих сообщений
- `notifications` - для отправки нотификаций

Процесс 1 слушает API телеграма.
Когда приходит сообщение, он посылает его в очередь rabbitmq
(в отдельном потоке), после чего продолжает слушать API.

Процессы 2n (workers) слушают входящие сообщения от API и обрабатывают
их по мере поступления. Отвечают на сообщения, создают напоминания в БД.

Процесс 3 запрашивает уведомления из БД раз в минуту
и ставит задачи в очередь.

Процессы 4n (workers) слушают очередь.
