# Детализация портов, связей и интерфейсов для E-Library

## ЧАСТЬ 1: ПОРТЫ КОМПОНЕНТОВ

---

### 1.1 КОМПОНЕНТЫ ВЕРХНЕГО УРОВНЯ

**ClientSubsystem (Клиентская подсистема)**

| Порт           | Направление | Интерфейс                         | Описание               |
| -------------- | ----------- | --------------------------------- | ---------------------- |
| HTTPRequestOut | Out         | ISearchQuery, IBookContentRequest | Исходящие HTTP запросы |
| HTTPResponseIn | In          | ISearchResults, IBookContent      | Входящие HTTP ответы   |
| AuthRequestOut | Out         | IUserCredentials                  | Запрос авторизации     |
| AuthResponseIn | In          | IAuthToken                        | Ответ с токеном        |
| WebSocketOut   | Out         | IAnalyticsEvent                   | Исходящий WebSocket    |
| WebSocketIn    | In          | INotification                     | Входящий WebSocket     |

**ServerSubsystem (Серверная подсистема)**

| Порт              | Направление | Интерфейс                         | Описание              |
| ----------------- | ----------- | --------------------------------- | --------------------- |
| HTTPRequestIn     | In          | ISearchQuery, IBookContentRequest | Входящие HTTP запросы |
| HTTPResponseOut   | Out         | ISearchResults, IBookContent      | Исходящие HTTP ответы |
| AuthRequestIn     | In          | IUserCredentials                  | Запрос авторизации    |
| AuthResponseOut   | Out         | IAuthToken                        | Ответ с токеном       |
| WebSocketIn       | In          | IAnalyticsEvent                   | Входящий WebSocket    |
| WebSocketOut      | Out         | INotification                     | Исходящий WebSocket   |
| LDAPRequestOut    | Out         | IUserCredentials                  | К внешнему LDAP       |
| LDAPResponseIn    | In          | IUserProfile                      | От внешнего LDAP      |
| PaymentRequestOut | Out         | —                                 | К платёжной системе   |
| PaymentResponseIn | In          | —                                 | От платёжной системы  |
| EmailRequestOut   | Out         | INotification                     | К почтовому сервису   |
| MetricsOut        | Out         | ISystemMetrics                    | К мониторингу         |

**ExternalSystems (Внешние системы)**


| Порт               | Направление | Интерфейс        | Описание   |
| ------------------ | ----------- | ---------------- | ---------- |
| LDAPRequestIn      | In          | IUserCredentials | От сервера |
| LDAPResponseOut    | Out         | IUserProfile     | К серверу  |
| PaymentRequestIn   | In          | —                | От сервера |
| PaymentResponseOut | Out         | —                | К серверу  |
| EmailRequestIn     | In          | INotification    | От сервера |
| PushRequestIn      | In          | INotification    | От сервера |

**MonitoringInfrastructure (Мониторинг)**

| Порт      | Направление | Интерфейс      | Описание         |
| --------- | ----------- | -------------- | ---------------- |
| MetricsIn | In          | ISystemMetrics | Входящие метрики |
| LogsIn    | In          | —              | Входящие логи    |
| AlertOut  | Out         | INotification  | Исходящие алерты |

---

### 1.2 КЛИЕНТСКАЯ ПОДСИСТЕМА — ВЛОЖЕННЫЕ КОМПОНЕНТЫ

#### Presentation Layer

**WebApplication**

| Порт | Направление | Интерфейс |
|------|-------------|-----------|
| UserInputIn | In | — |
| DisplayOut | Out | — |
| ToAuthClientOut | Out | IUserCredentials |
| FromAuthClientIn | In | IAuthToken |
| ToSearchClientOut | Out | ISearchQuery |
| FromSearchClientIn | In | ISearchResults |
| ToBookViewerOut | Out | IBookContentRequest |
| FromBookViewerIn | In | IBookContent |

**MobileApplication**

| Порт | Направление | Интерфейс |
|------|-------------|-----------|
| UserInputIn | In | — |
| DisplayOut | Out | — |
| ToAuthClientOut | Out | IUserCredentials |
| FromAuthClientIn | In | IAuthToken |
| ToSearchClientOut | Out | ISearchQuery |
| FromSearchClientIn | In | ISearchResults |
| ToBookViewerOut | Out | IBookContentRequest |
| FromBookViewerIn | In | IBookContent |
| PushNotificationIn | In | INotification |

**DesktopReader**

| Порт | Направление | Интерфейс |
|------|-------------|-----------|
| ToBookViewerOut | Out | IBookContentRequest |
| FromBookViewerIn | In | IBookContent |
| ToOfflineStorageOut | Out | IBookContent |
| FromOfflineStorageIn | In | IBookContent |

---

#### Application Layer (Client)

**AuthenticationClient**

| Порт | Направление | Интерфейс |
|------|-------------|-----------|
| CredentialsIn | In | IUserCredentials |
| TokenOut | Out | IAuthToken |
| ToServerAuthOut | Out | IUserCredentials |
| FromServerAuthIn | In | IAuthToken |
| ToCacheOut | Out | IAuthToken |
| FromCacheIn | In | IAuthToken |

**SearchEngineClient**

| Порт | Направление | Интерфейс |
|------|-------------|-----------|
| QueryIn | In | ISearchQuery |
| ResultsOut | Out | ISearchResults |
| ToServerSearchOut | Out | ISearchQuery |
| FromServerSearchIn | In | ISearchResults |
| ToCacheOut | Out | ISearchResults |
| FromCacheIn | In | ISearchResults |

**BookViewer**

| Порт | Направление | Интерфейс |
|------|-------------|-----------|
| ContentRequestIn | In | IBookContentRequest |
| ContentOut | Out | IBookContent |
| ToDownloadMgrOut | Out | IBookContentRequest |
| FromDownloadMgrIn | In | IBookContent |
| ToBookmarkMgrOut | Out | IBooking |
| FromBookmarkMgrIn | In | IBooking |
| ToProgressTrackerOut | Out | IAnalyticsEvent |

**DownloadManager**

| Порт | Направление | Интерфейс |
|------|-------------|-----------|
| RequestIn | In | IBookContentRequest |
| ContentOut | Out | IBookContent |
| ToServerContentOut | Out | IBookContentRequest |
| FromServerContentIn | In | IBookContent |
| ToOfflineStorageOut | Out | IBookContent |

**BookmarkManager**

| Порт | Направление | Интерфейс |
|------|-------------|-----------|
| BookmarkIn | In | IBooking |
| BookmarkOut | Out | IBooking |
| ToLocalCacheOut | Out | IBooking |
| FromLocalCacheIn | In | IBooking |
| ToServerSyncOut | Out | IBooking |
| FromServerSyncIn | In | IBooking |

**ReadingProgressTracker**

| Порт | Направление | Интерфейс |
|------|-------------|-----------|
| ProgressEventIn | In | IAnalyticsEvent |
| ToServerAnalyticsOut | Out | IAnalyticsEvent |
| ToLocalCacheOut | Out | IAnalyticsEvent |

---

#### Data Layer (Client)

**LocalCache**

| Порт | Направление | Интерфейс |
|------|-------------|-----------|
| WriteIn | In | ISearchResults, IAuthToken, IBooking |
| ReadOut | Out | ISearchResults, IAuthToken, IBooking |
| QueryIn | In | — |
| ToSyncEngineOut | Out | — |

**OfflineStorage**

| Порт | Направление | Интерфейс |
|------|-------------|-----------|
| WriteIn | In | IBookContent |
| ReadOut | Out | IBookContent |
| ToSyncEngineOut | Out | IBookContent |

**SyncEngine**

| Порт | Направление | Интерфейс |
|------|-------------|-----------|
| FromCacheIn | In | — |
| FromStorageIn | In | IBookContent |
| ToServerSyncOut | Out | IBooking, IAnalyticsEvent |
| FromServerSyncIn | In | IBooking |

---

### 1.3 СЕРВЕРНАЯ ПОДСИСТЕМА — ВЛОЖЕННЫЕ КОМПОНЕНТЫ

#### API Gateway Layer

**RateLimiter**

| Порт        | Направление | Интерфейс                      |
| ----------- | ----------- | ------------------------------ |
| RequestIn   | In          | IUserCredentials, ISearchQuery |
| RequestOut  | Out         | IUserCredentials, ISearchQuery |
| ToRedisOut  | Out         | —                              |
| FromRedisIn | In          | —                              |

**LoadBalancer**

| Порт          | Направление | Интерфейс                      |
| ------------- | ----------- | ------------------------------ |
| RequestIn     | In          | IUserCredentials, ISearchQuery |
| RequestOut    | Out         | IUserCredentials, ISearchQuery |
| HealthCheckIn | In          | ISystemMetrics                 |

**RequestValidator**

| Порт | Направление | Интерфейс |
|------|-------------|-----------|
| RequestIn | In | IUserCredentials, ISearchQuery, IBookContentRequest |
| ValidRequestOut | Out | IUserCredentials, ISearchQuery, IBookContentRequest |
| ErrorOut | Out | — |

**AuthMiddleware**

| Порт                 | Направление | Интерфейс    |
| -------------------- | ----------- | ------------ |
| RequestIn            | In          | IAuthToken   |
| AuthorizedRequestOut | Out         | IUserProfile |
| ToAuthServiceOut     | Out         | IAuthToken   |
| FromAuthServiceIn    | In          | IUserProfile |

**ResponseCache**

| Порт | Направление | Интерфейс |
|------|-------------|-----------|
| RequestIn | In | ISearchQuery |
| CachedResponseOut | Out | ISearchResults |
| ToRedisOut | Out | ISearchResults |
| FromRedisIn | In | ISearchResults |
| ToServiceLayerOut | Out | ISearchQuery |
| FromServiceLayerIn | In | ISearchResults |

---

#### Service Layer

**AuthenticationService**

| Порт | Направление | Интерфейс |
|------|-------------|-----------|
| CredentialsIn | In | IUserCredentials |
| TokenOut | Out | IAuthToken |
| ProfileRequestIn | In | IAuthToken |
| ProfileOut | Out | IUserProfile |
| ToPostgresOut | Out | IUserCredentials |
| FromPostgresIn | In | IUserProfile |
| ToLDAPOut | Out | IUserCredentials |
| FromLDAPIn | In | IUserProfile |
| ToRedisSessionOut | Out | IAuthToken |
| FromRedisSessionIn | In | IAuthToken |

**UserService**

| Порт | Направление | Интерфейс |
|------|-------------|-----------|
| ProfileRequestIn | In | — |
| ProfileOut | Out | IUserProfile |
| UpdateProfileIn | In | IUserProfile |
| ToPostgresOut | Out | IUserProfile |
| FromPostgresIn | In | IUserProfile |
| ToNotificationOut | Out | INotification |

**CatalogService**

| Порт | Направление | Интерфейс |
|------|-------------|-----------|
| BookQueryIn | In | — |
| BookMetadataOut | Out | IBookMetadata |
| AddBookIn | In | IBookMetadata |
| ToMongoOut | Out | IBookMetadata |
| FromMongoIn | In | IBookMetadata |
| ToElasticIndexOut | Out | IBookMetadata |

**SearchService**

| Порт | Направление | Интерфейс |
|------|-------------|-----------|
| QueryIn | In | ISearchQuery |
| ResultsOut | Out | ISearchResults |
| ToElasticOut | Out | ISearchQuery |
| FromElasticIn | In | ISearchResults |
| ToRedisOut | Out | ISearchResults |
| FromRedisIn | In | ISearchResults |

**BookingService**

| Порт | Направление | Интерфейс |
|------|-------------|-----------|
| BookingRequestIn | In | IBooking |
| BookingResponseOut | Out | IBooking |
| ToPostgresOut | Out | IBooking |
| FromPostgresIn | In | IBooking |
| ToNotificationOut | Out | INotification |
| ToAnalyticsOut | Out | IAnalyticsEvent |

**ContentDeliveryService**

| Порт | Направление | Интерфейс |
|------|-------------|-----------|
| ContentRequestIn | In | IBookContentRequest |
| ContentOut | Out | IBookContent |
| ToS3Out | Out | IBookContentRequest |
| FromS3In | In | IBookContent |
| ToRedisOut | Out | IBookContent |
| FromRedisIn | In | IBookContent |

**NotificationService**

| Порт | Направление | Интерфейс |
|------|-------------|-----------|
| NotificationIn | In | INotification |
| ToEmailServiceOut | Out | INotification |
| ToPushServiceOut | Out | INotification |
| ToRabbitMQOut | Out | INotification |
| FromRabbitMQIn | In | INotification |
| ToPostgresOut | Out | INotification |

**AnalyticsService**

| Порт | Направление | Интерфейс |
|------|-------------|-----------|
| EventIn | In | IAnalyticsEvent |
| ToKafkaOut | Out | IAnalyticsEvent |
| FromKafkaIn | In | IAnalyticsEvent |
| ToClickHouseOut | Out | IAnalyticsEvent |

**ReportService**

| Порт | Направление | Интерфейс |
|------|-------------|-----------|
| ReportRequestIn | In | — |
| ReportOut | Out | — |
| FromClickHouseIn | In | — |
| FromPostgresIn | In | — |

**RecommendationService**

| Порт | Направление | Интерфейс |
|------|-------------|-----------|
| UserIdIn | In | — |
| RecommendationsOut | Out | IBookMetadata |
| FromClickHouseIn | In | IAnalyticsEvent |
| FromMongoIn | In | IBookMetadata |
| ToRedisOut | Out | IBookMetadata |
| FromRedisIn | In | IBookMetadata |

---

#### Data Layer (Server)

**PostgreSQLCluster**

| Порт | Направление | Интерфейс |
|------|-------------|-----------|
| QueryIn | In | IUserProfile, IBooking, INotification |
| ResultOut | Out | IUserProfile, IBooking, INotification |
| ReplicationOut | Out | — |

**MongoDBCluster**

| Порт | Направление | Интерфейс |
|------|-------------|-----------|
| QueryIn | In | IBookMetadata |
| ResultOut | Out | IBookMetadata |
| ReplicationOut | Out | — |

**ElasticsearchCluster**

| Порт | Направление | Интерфейс |
|------|-------------|-----------|
| SearchQueryIn | In | ISearchQuery |
| SearchResultOut | Out | ISearchResults |
| IndexIn | In | IBookMetadata |

**RedisCluster**

| Порт | Направление | Интерфейс |
|------|-------------|-----------|
| CacheWriteIn | In | ISearchResults, IAuthToken, IBookContent |
| CacheReadOut | Out | ISearchResults, IAuthToken, IBookContent |
| SessionIn | In | IAuthToken |
| SessionOut | Out | IAuthToken |
| RateLimitIn | In | — |
| RateLimitOut | Out | — |

**ClickHouseCluster**

| Порт | Направление | Интерфейс |
|------|-------------|-----------|
| InsertIn | In | IAnalyticsEvent |
| QueryIn | In | — |
| ResultOut | Out | IAnalyticsEvent |

**ObjectStorage (S3/MinIO)**

| Порт | Направление | Интерфейс |
|------|-------------|-----------|
| UploadIn | In | IBookContent |
| DownloadRequestIn | In | IBookContentRequest |
| DownloadOut | Out | IBookContent |
| DeleteIn | In | — |

---

#### Message Queue Layer

**RabbitMQCluster**

| Порт | Направление | Интерфейс |
|------|-------------|-----------|
| PublishIn | In | INotification |
| ConsumeOut | Out | INotification |
| EmailQueueOut | Out | INotification |
| PushQueueOut | Out | INotification |

**KafkaCluster**

| Порт | Направление | Интерфейс |
|------|-------------|-----------|
| ProduceIn | In | IAnalyticsEvent |
| ConsumeOut | Out | IAnalyticsEvent |
| TopicAnalyticsOut | Out | IAnalyticsEvent |

---

### 1.4 ВНЕШНИЕ СИСТЕМЫ — ВЛОЖЕННЫЕ КОМПОНЕНТЫ

**UniversityLDAP**

| Порт | Направление | Интерфейс |
|------|-------------|-----------|
| AuthRequestIn | In | IUserCredentials |
| UserDataOut | Out | IUserProfile |

**PaymentGateway**

| Порт | Направление | Интерфейс |
|------|-------------|-----------|
| PaymentRequestIn | In | — |
| PaymentResultOut | Out | — |

**EmailService**

| Порт | Направление | Интерфейс |
|------|-------------|-----------|
| SendRequestIn | In | INotification |
| StatusOut | Out | — |

**PushNotificationService**

| Порт | Направление | Интерфейс |
|------|-------------|-----------|
| PushRequestIn | In | INotification |
| StatusOut | Out | — |

**ISBNDatabase**

| Порт | Направление | Интерфейс |
|------|-------------|-----------|
| ISBNQueryIn | In | — |
| MetadataOut | Out | IBookMetadata |

**LMSIntegration**

| Порт | Направление | Интерфейс |
|------|-------------|-----------|
| CourseRequestIn | In | — |
| ReadingListOut | Out | IBookMetadata |

---

### 1.5 МОНИТОРИНГ — ВЛОЖЕННЫЕ КОМПОНЕНТЫ

**Prometheus**

| Порт | Направление | Интерфейс |
|------|-------------|-----------|
| MetricsIn | In | ISystemMetrics |
| ToGrafanaOut | Out | ISystemMetrics |
| ToAlertManagerOut | Out | ISystemMetrics |

**Grafana**

| Порт | Направление | Интерфейс |
|------|-------------|-----------|
| MetricsIn | In | ISystemMetrics |
| DashboardOut | Out | — |

**ELKStack**

| Порт | Направление | Интерфейс |
|------|-------------|-----------|
| LogsIn | In | — |
| ToGrafanaOut | Out | — |

**Jaeger**

| Порт | Направление | Интерфейс |
|------|-------------|-----------|
| TracesIn | In | — |
| ToGrafanaOut | Out | — |

**Alertmanager**

| Порт | Направление | Интерфейс |
|------|-------------|-----------|
| AlertIn | In | ISystemMetrics |
| NotificationOut | Out | INotification |

**HealthCheckService**

| Порт              | Направление | Интерфейс      |
| ----------------- | ----------- | -------------- |
| HealthRequestOut  | Out         | —              |
| HealthResponseIn  | In          | ISystemMetrics |
| ToAlertManagerOut | Out         | ISystemMetrics |

---

## ЧАСТЬ 2: СВЯЗИ МЕЖДУ КОМПОНЕНТАМИ

### 2.1 СВЯЗИ ВЕРХНЕГО УРОВНЯ

| Источник        | Порт источника  | →   | Назначение               | Порт назначения |
| --------------- | --------------- | --- | ------------------------ | --------------- |
| ClientSubsystem | HTTPRequestOut  | →   | ServerSubsystem          | HTTPRequestIn   |
| ServerSubsystem | HTTPResponseOut | →   | ClientSubsystem          | HTTPResponseIn  |
| ClientSubsystem | AuthRequestOut  | →   | ServerSubsystem          | AuthRequestIn   |
| ServerSubsystem | AuthResponseOut | →   | ClientSubsystem          | AuthResponseIn  |
| ClientSubsystem | WebSocketOut    | →   | ServerSubsystem          | WebSocketIn     |
| ServerSubsystem | WebSocketOut    | →   | ClientSubsystem          | WebSocketIn     |
| ServerSubsystem | LDAPRequestOut  | →   | ExternalSystems          | LDAPRequestIn   |
| ExternalSystems | LDAPResponseOut | →   | ServerSubsystem          | LDAPResponseIn  |
| ServerSubsystem | EmailRequestOut | →   | ExternalSystems          | EmailRequestIn  |
| ServerSubsystem | MetricsOut      | →   | MonitoringInfrastructure | MetricsIn       |

---

### 2.2 СВЯЗИ ВНУТРИ КЛИЕНТСКОЙ ПОДСИСТЕМЫ

#### Presentation → Application Layer

| Источник | Порт | → | Назначение | Порт |
|----------|------|---|------------|------|
| WebApplication | ToAuthClientOut | → | AuthenticationClient | CredentialsIn |
| AuthenticationClient | TokenOut | → | WebApplication | FromAuthClientIn |
| WebApplication | ToSearchClientOut | → | SearchEngineClient | QueryIn |
| SearchEngineClient | ResultsOut | → | WebApplication | FromSearchClientIn |
| WebApplication | ToBookViewerOut | → | BookViewer | ContentRequestIn |
| BookViewer | ContentOut | → | WebApplication | FromBookViewerIn |
| MobileApplication | ToAuthClientOut | → | AuthenticationClient | CredentialsIn |
| MobileApplication | ToSearchClientOut | → | SearchEngineClient | QueryIn |
| MobileApplication | ToBookViewerOut | → | BookViewer | ContentRequestIn |
| DesktopReader | ToBookViewerOut | → | BookViewer | ContentRequestIn |

#### Application Layer внутренние

| Источник | Порт | → | Назначение | Порт |
|----------|------|---|------------|------|
| BookViewer | ToDownloadMgrOut | → | DownloadManager | RequestIn |
| DownloadManager | ContentOut | → | BookViewer | FromDownloadMgrIn |
| BookViewer | ToBookmarkMgrOut | → | BookmarkManager | BookmarkIn |
| BookmarkManager | BookmarkOut | → | BookViewer | FromBookmarkMgrIn |
| BookViewer | ToProgressTrackerOut | → | ReadingProgressTracker | ProgressEventIn |

#### Application → Data Layer

| Источник | Порт | → | Назначение | Порт |
|----------|------|---|------------|------|
| AuthenticationClient | ToCacheOut | → | LocalCache | WriteIn |
| LocalCache | ReadOut | → | AuthenticationClient | FromCacheIn |
| SearchEngineClient | ToCacheOut | → | LocalCache | WriteIn |
| LocalCache | ReadOut | → | SearchEngineClient | FromCacheIn |
| DownloadManager | ToOfflineStorageOut | → | OfflineStorage | WriteIn |
| OfflineStorage | ReadOut | → | DesktopReader | FromOfflineStorageIn |
| BookmarkManager | ToLocalCacheOut | → | LocalCache | WriteIn |
| LocalCache | ReadOut | → | BookmarkManager | FromLocalCacheIn |
| ReadingProgressTracker | ToLocalCacheOut | → | LocalCache | WriteIn |

#### Data Layer внутренние

| Источник | Порт | → | Назначение | Порт |
|----------|------|---|------------|------|
| LocalCache | ToSyncEngineOut | → | SyncEngine | FromCacheIn |
| OfflineStorage | ToSyncEngineOut | → | SyncEngine | FromStorageIn |

---

### 2.3 СВЯЗИ ВНУТРИ СЕРВЕРНОЙ ПОДСИСТЕМЫ

#### API Gateway внутренние

| Источник | Порт | → | Назначение | Порт |
|----------|------|---|------------|------|
| RateLimiter | RequestOut | → | LoadBalancer | RequestIn |
| LoadBalancer | RequestOut | → | RequestValidator | RequestIn |
| RequestValidator | ValidRequestOut | → | AuthMiddleware | RequestIn |
| AuthMiddleware | AuthorizedRequestOut | → | ResponseCache | RequestIn |

#### API Gateway → Service Layer

| Источник | Порт | → | Назначение | Порт |
|----------|------|---|------------|------|
| ResponseCache | ToServiceLayerOut | → | SearchService | QueryIn |
| SearchService | ResultsOut | → | ResponseCache | FromServiceLayerIn |
| AuthMiddleware | ToAuthServiceOut | → | AuthenticationService | ProfileRequestIn |
| AuthenticationService | ProfileOut | → | AuthMiddleware | FromAuthServiceIn |

#### Service Layer внутренние

| Источник | Порт | → | Назначение | Порт |
|----------|------|---|------------|------|
| BookingService | ToNotificationOut | → | NotificationService | NotificationIn |
| BookingService | ToAnalyticsOut | → | AnalyticsService | EventIn |
| UserService | ToNotificationOut | → | NotificationService | NotificationIn |
| CatalogService | ToElasticIndexOut | → | SearchService | QueryIn |

#### Service Layer → Data Layer

| Источник | Порт | → | Назначение | Порт |
|----------|------|---|------------|------|
| AuthenticationService | ToPostgresOut | → | PostgreSQLCluster | QueryIn |
| PostgreSQLCluster | ResultOut | → | AuthenticationService | FromPostgresIn |
| AuthenticationService | ToRedisSessionOut | → | RedisCluster | SessionIn |
| RedisCluster | SessionOut | → | AuthenticationService | FromRedisSessionIn |
| UserService | ToPostgresOut | → | PostgreSQLCluster | QueryIn |
| PostgreSQLCluster | ResultOut | → | UserService | FromPostgresIn |
| CatalogService | ToMongoOut | → | MongoDBCluster | QueryIn |
| MongoDBCluster | ResultOut | → | CatalogService | FromMongoIn |
| SearchService | ToElasticOut | → | ElasticsearchCluster | SearchQueryIn |
| ElasticsearchCluster | SearchResultOut | → | SearchService | FromElasticIn |
| SearchService | ToRedisOut | → | RedisCluster | CacheWriteIn |
| RedisCluster | CacheReadOut | → | SearchService | FromRedisIn |
| BookingService | ToPostgresOut | → | PostgreSQLCluster | QueryIn |
| PostgreSQLCluster | ResultOut | → | BookingService | FromPostgresIn |
| ContentDeliveryService | ToS3Out | → | ObjectStorage | DownloadRequestIn |
| ObjectStorage | DownloadOut | → | ContentDeliveryService | FromS3In |
| ContentDeliveryService | ToRedisOut | → | RedisCluster | CacheWriteIn |
| RedisCluster | CacheReadOut | → | ContentDeliveryService | FromRedisIn |
| NotificationService | ToPostgresOut | → | PostgreSQLCluster | QueryIn |
| AnalyticsService | ToClickHouseOut | → | ClickHouseCluster | InsertIn |
| ReportService | FromClickHouseIn | ← | ClickHouseCluster | ResultOut |
| ReportService | FromPostgresIn | ← | PostgreSQLCluster | ResultOut |
| RecommendationService | FromClickHouseIn | ← | ClickHouseCluster | ResultOut |
| RecommendationService | FromMongoIn | ← | MongoDBCluster | ResultOut |
| RecommendationService | ToRedisOut | → | RedisCluster | CacheWriteIn |
| RedisCluster | CacheReadOut | → | RecommendationService | FromRedisIn |

#### Service Layer → Message Queue

| Источник | Порт | → | Назначение | Порт |
|----------|------|---|------------|------|
| NotificationService | ToRabbitMQOut | → | RabbitMQCluster | PublishIn |
| RabbitMQCluster | ConsumeOut | → | NotificationService | FromRabbitMQIn |
| AnalyticsService | ToKafkaOut | → | KafkaCluster | ProduceIn |
| KafkaCluster | ConsumeOut | → | AnalyticsService | FromKafkaIn |

#### API Gateway → Data Layer

| Источник | Порт | → | Назначение | Порт |
|----------|------|---|------------|------|
| RateLimiter | ToRedisOut | → | RedisCluster | RateLimitIn |
| RedisCluster | RateLimitOut | → | RateLimiter | FromRedisIn |
| ResponseCache | ToRedisOut | → | RedisCluster | CacheWriteIn |
| RedisCluster | CacheReadOut | → | ResponseCache | FromRedisIn |

---

### 2.4 СВЯЗИ МЕЖДУ ПОДСИСТЕМАМИ (ВЛОЖЕННЫЕ КОМПОНЕНТЫ)

#### Клиент → Сервер (через границы подсистем)

**Важно:** Эти связи проходят через порты родительских компонентов

| Клиентский компонент | → | Серверный компонент | Интерфейс |
|---------------------|---|---------------------|-----------|
| AuthenticationClient.ToServerAuthOut | → | AuthenticationService.CredentialsIn | IUserCredentials |
| AuthenticationService.TokenOut | → | AuthenticationClient.FromServerAuthIn | IAuthToken |
| SearchEngineClient.ToServerSearchOut | → | SearchService.QueryIn | ISearchQuery |
| SearchService.ResultsOut | → | SearchEngineClient.FromServerSearchIn | ISearchResults |
| DownloadManager.ToServerContentOut | → | ContentDeliveryService.ContentRequestIn | IBookContentRequest |
| ContentDeliveryService.ContentOut | → | DownloadManager.FromServerContentIn | IBookContent |
| BookmarkManager.ToServerSyncOut | → | BookingService.BookingRequestIn | IBooking |
| BookingService.BookingResponseOut | → | BookmarkManager.FromServerSyncIn | IBooking |
| ReadingProgressTracker.ToServerAnalyticsOut | → | AnalyticsService.EventIn | IAnalyticsEvent |
| SyncEngine.ToServerSyncOut | → | BookingService.BookingRequestIn | IBooking |
| BookingService.BookingResponseOut | → | SyncEngine.FromServerSyncIn | IBooking |

#### Сервер → Внешние системы

| Серверный компонент | → | Внешний компонент | Интерфейс |
|--------------------|---|-------------------|-----------|
| AuthenticationService.ToLDAPOut | → | UniversityLDAP.AuthRequestIn | IUserCredentials |
| UniversityLDAP.UserDataOut | → | AuthenticationService.FromLDAPIn | IUserProfile |
| NotificationService.ToEmailServiceOut | → | EmailService.SendRequestIn | INotification |
| NotificationService.ToPushServiceOut | → | PushNotificationService.PushRequestIn | INotification |
| RabbitMQCluster.EmailQueueOut | → | EmailService.SendRequestIn | INotification |
| RabbitMQCluster.PushQueueOut | → | PushNotificationService.PushRequestIn | INotification |
| CatalogService.ToISBNOut | → | ISBNDatabase.ISBNQueryIn | — |
| ISBNDatabase.MetadataOut | → | CatalogService.FromISBNIn | IBookMetadata |

#### Сервер → Мониторинг

| Серверный компонент               | →   | Компонент мониторинга               | Интерфейс      |
| --------------------------------- | --- | ----------------------------------- | -------------- |
| AuthenticationService.MetricsOut  | →   | Prometheus.MetricsIn                | ISystemMetrics |
| SearchService.MetricsOut          | →   | Prometheus.MetricsIn                | ISystemMetrics |
| BookingService.MetricsOut         | →   | Prometheus.MetricsIn                | ISystemMetrics |
| ContentDeliveryService.MetricsOut | →   | Prometheus.MetricsIn                | ISystemMetrics |
| HealthCheckService.ToServicesOut  | →   | LoadBalancer.HealthCheckIn          | —              |
| LoadBalancer.HealthResponseOut    | →   | HealthCheckService.HealthResponseIn | ISystemMetrics |

---

### 2.5 СВЯЗИ ВНУТРИ МОНИТОРИНГА

| Источник | Порт | → | Назначение | Порт |
|----------|------|---|------------|------|
| Prometheus | ToGrafanaOut | → | Grafana | MetricsIn |
| Prometheus | ToAlertManagerOut | → | Alertmanager | AlertIn |
| ELKStack | ToGrafanaOut | → | Grafana | DashboardOut |
| Jaeger | ToGrafanaOut | → | Grafana | DashboardOut |
| HealthCheckService | ToAlertManagerOut | → | Alertmanager | AlertIn |
| Alertmanager | NotificationOut | → | (к NotificationService через родительские порты) | INotification |

---

### 2.6 СВЯЗИ ВНУТРИ ВНЕШНИХ СИСТЕМ

Внешние системы обычно не связаны между собой напрямую, каждый компонент работает независимо и взаимодействует только с серверной подсистемой.

---

## ЧАСТЬ 3: КАК СОЗДАВАТЬ В SYSTEM COMPOSER ВРУЧНУЮ

### Шаг 1: Создание портов

1. Откройте архитектуру компонента (двойной клик)
2. На панели инструментов найдите "Add Port" или через контекстное меню
3. Укажите:
   - Имя порта
   - Направление (In/Out)
4. После создания порта выделите его и в Property Inspector назначьте интерфейс из словаря данных

### Шаг 2: Назначение интерфейса порту

1. Убедитесь что словарь данных привязан к модели (Model → Link to Data Dictionary)
2. Выделите порт
3. В Property Inspector найдите поле "Interface"
4. Выберите нужный интерфейс из списка (например IUserCredentials)

### Шаг 3: Создание связей

1. Находясь в нужной архитектуре, найдите два порта которые нужно соединить
2. Зажмите левую кнопку мыши на выходном порту
3. Протяните линию к входному порту
4. Отпустите кнопку — связь создана

### Шаг 4: Связи между вложенными компонентами разных подсистем

**Вариант А: Через делегирование портов**


1. Создайте порт на границе дочернего компонента (например AuthenticationClient)
2. Создайте аналогичный порт на границе родительского компонента (ClientSubsystem)
3. Внутри родительской архитектуры соедините порт дочернего компонента с портом на границе родителя
4. Повторите для серверной стороны
5. На верхнем уровне соедините порты родительских компонентов

**Вариант Б: Через ссылки на архитектуры**


1. Создайте отдельную модель для переиспользуемой архитектуры
2. Добавьте ссылку на эту архитектуру в обоих местах
3. Порты будут автоматически согласованы

### Шаг 5: Применение стереотипа к связи

1. Выделите созданную связь (коннектор)
2. В Property Inspector найдите "Stereotypes"
3. Нажмите "Apply Stereotype"
4. Выберите нужный (например SecureConnection или InternalConnection)
5. Заполните свойства стереотипа

---

## ЧАСТЬ 4: ПРОВЕРОЧНЫЙ ЧЕКЛИСТ

После создания всех связей проверьте:

- [ ] Каждый порт имеет назначенный интерфейс
- [ ] Соединённые порты используют совместимые интерфейсы
- [ ] Все входящие данные имеют источник
- [ ] Все выходящие данные имеют получателя
- [ ] Связи между подсистемами проходят через делегированные порты
- [ ] Стереотипы применены к связям (SecureConnection для внешних, InternalConnection для внутренних)