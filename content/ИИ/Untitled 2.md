В приложенном JSON описана архитектура **AdaptiveLearningGame** (компоненты GameClient/GameLogicCore и т.п.) — она не соответствует вашей теме про веб‑ГИС для археологии. Если ваша задача — **получить аналогичное (в стиле MATLAB System Composer) описание структуры и требований, но уже для веб‑ГИС**, ниже даю адаптированный вариант (компоненты/порты/соединения/интерфейсы/требования) под ваш стек: Vue 3 + Express + PostGIS + Redis + Yandex Maps + JWT + PDF.

## 1) Предложенная компонентная декомпозиция (логически)
- **WebClient (SPA)**: карта, фильтры, просмотр карточки памятника.
- **AdminPanel (в составе SPA или отдельный модуль UI)**: CRUD, справочники, загрузка PDF.
- **BackendAPI (Express)**: REST API, валидация, агрегация данных.
- **AuthModule (JWT)**: логин/refresh, роли.
- **HeritageCatalogService**: бизнес‑логика памятников/эпох/типов.
- **GeoService**: пространственные запросы PostGIS, кластеры/выборки по bbox, назначение района.
- **FileService**: хранение/выдача PDF (локально/S3‑подобно).
- **SearchIntegrationService**: формирование ссылок/запросов в Elibrary/Google по координатам.
- **PostgreSQL/PostGIS**: основное хранилище.
- **RedisCache**: кэширование фильтров/списков/частых запросов.
- **YandexMapsAPI**: отображение тайлов/слоёв, кластеризация (частично на фронте, частично данные готовит бэкенд).

## 2) Пример JSON в формате, близком к вашему экспорту
> Это **шаблон**, который можно расширять (например, добавить роли, аудит, версии записей, импорт из CSV/GeoJSON и т.д.).

```json
{
  "Name": "ArchaeologyWebGIS",
  "ExportDate": "10-Jan-2026 17:19:18",
  "Structure": {
    "Components": [
      {
        "Name": "WebClientSPA",
        "Type": "Component",
        "Ports": [
          { "Name": "outApiRequest", "Direction": "Output", "Interface": "HttpRestInterface", "Stereotype": "" },
          { "Name": "inApiResponse", "Direction": "Input", "Interface": "HttpRestInterface", "Stereotype": "" },
          { "Name": "outMapTilesReq", "Direction": "Output", "Interface": "MapProviderInterface", "Stereotype": "" },
          { "Name": "inMapEvents", "Direction": "Input", "Interface": "MapEventsInterface", "Stereotype": "" }
        ],
        "Internals": {
          "Components": [
            {
              "Name": "MapModule",
              "Type": "Component",
              "Ports": [
                { "Name": "inFeatures", "Direction": "Input", "Interface": "GeoFeaturesInterface", "Stereotype": "" },
                { "Name": "outViewport", "Direction": "Output", "Interface": "ViewportInterface", "Stereotype": "" },
                { "Name": "outFeatureSelect", "Direction": "Output", "Interface": "FeatureSelectInterface", "Stereotype": "" }
              ],
              "Properties": { "Provider": "YandexMapsAPI 2.1" }
            },
            {
              "Name": "FilterPanel",
              "Type": "Component",
              "Ports": [
                { "Name": "outFilter", "Direction": "Output", "Interface": "FilterQueryInterface", "Stereotype": "" }
              ],
              "Properties": {}
            },
            {
              "Name": "AdminPanel",
              "Type": "Component",
              "Ports": [
                { "Name": "outCrudRequest", "Direction": "Output", "Interface": "CrudInterface", "Stereotype": "" },
                { "Name": "inCrudResponse", "Direction": "Input", "Interface": "CrudInterface", "Stereotype": "" }
              ],
              "Properties": { "Auth": "JWT" }
            }
          ],
          "Connections": [
            { "Source": "FilterPanel/outFilter", "Target": "BOUNDARY/outApiRequest", "Interface": "FilterQueryInterface", "Name": "Conn" },
            { "Source": "MapModule/outViewport", "Target": "BOUNDARY/outApiRequest", "Interface": "ViewportInterface", "Name": "Conn" },
            { "Source": "AdminPanel/outCrudRequest", "Target": "BOUNDARY/outApiRequest", "Interface": "CrudInterface", "Name": "Conn" }
          ],
          "BoundaryPorts": [
            { "Name": "outApiRequest", "Direction": "Output", "Interface": "HttpRestInterface", "IsBoundary": true },
            { "Name": "inApiResponse", "Direction": "Input", "Interface": "HttpRestInterface", "IsBoundary": true },
            { "Name": "outMapTilesReq", "Direction": "Output", "Interface": "MapProviderInterface", "IsBoundary": true },
            { "Name": "inMapEvents", "Direction": "Input", "Interface": "MapEventsInterface", "IsBoundary": true }
          ]
        }
      },
      {
        "Name": "BackendAPI",
        "Type": "Component",
        "Ports": [
          { "Name": "inHttpRequest", "Direction": "Input", "Interface": "HttpRestInterface", "Stereotype": "" },
          { "Name": "outHttpResponse", "Direction": "Output", "Interface": "HttpRestInterface", "Stereotype": "" },
          { "Name": "outDbQuery", "Direction": "Output", "Interface": "SqlGeoQueryInterface", "Stereotype": "" },
          { "Name": "inDbResult", "Direction": "Input", "Interface": "SqlGeoQueryInterface", "Stereotype": "" },
          { "Name": "outCacheOps", "Direction": "Output", "Interface": "CacheInterface", "Stereotype": "" },
          { "Name": "inCacheOps", "Direction": "Input", "Interface": "CacheInterface", "Stereotype": "" },
          { "Name": "outFileOps", "Direction": "Output", "Interface": "FileStorageInterface", "Stereotype": "" }
        ],
        "Internals": {
          "Components": [
            {
              "Name": "AuthModule",
              "Type": "Component",
              "Ports": [
                { "Name": "inAuthReq", "Direction": "Input", "Interface": "AuthInterface", "Stereotype": "" },
                { "Name": "outAuthRes", "Direction": "Output", "Interface": "AuthInterface", "Stereotype": "" }
              ],
              "Properties": { "JWT": true }
            },
            {
              "Name": "HeritageCatalogService",
              "Type": "Component",
              "Ports": [
                { "Name": "inCrud", "Direction": "Input", "Interface": "CrudInterface", "Stereotype": "" },
                { "Name": "outCrud", "Direction": "Output", "Interface": "CrudInterface", "Stereotype": "" },
                { "Name": "outGeoQuery", "Direction": "Output", "Interface": "SqlGeoQueryInterface", "Stereotype": "" }
              ],
              "Properties": { "ORM": "Sequelize" }
            },
            {
              "Name": "GeoService",
              "Type": "Component",
              "Ports": [
                { "Name": "inViewport", "Direction": "Input", "Interface": "ViewportInterface", "Stereotype": "" },
                { "Name": "inFilter", "Direction": "Input", "Interface": "FilterQueryInterface", "Stereotype": "" },
                { "Name": "outGeoFeatures", "Direction": "Output", "Interface": "GeoFeaturesInterface", "Stereotype": "" },
                { "Name": "outGeoQuery", "Direction": "Output", "Interface": "SqlGeoQueryInterface", "Stereotype": "" }
              ],
              "Properties": { "PostGIS": true }
            },
            {
              "Name": "SearchIntegrationService",
              "Type": "Component",
              "Ports": [
                { "Name": "inSearchReq", "Direction": "Input", "Interface": "SearchRequestInterface", "Stereotype": "" },
                { "Name": "outSearchRes", "Direction": "Output", "Interface": "SearchResultInterface", "Stereotype": "" }
              ],
              "Properties": { "Providers": ["Elibrary", "Google"] }
            },
            {
              "Name": "FileService",
              "Type": "Component",
              "Ports": [
                { "Name": "inFileOps", "Direction": "Input", "Interface": "FileStorageInterface", "Stereotype": "" },
                { "Name": "outFileOps", "Direction": "Output", "Interface": "FileStorageInterface", "Stereotype": "" }
              ],
              "Properties": { "Types": ["PDF"] }
            }
          ],
          "Connections": [
            { "Source": "BOUNDARY/inHttpRequest", "Target": "AuthModule/inAuthReq", "Interface": "AuthInterface", "Name": "Conn" },
            { "Source": "BOUNDARY/inHttpRequest", "Target": "GeoService/inViewport", "Interface": "ViewportInterface", "Name": "Conn" },
            { "Source": "BOUNDARY/inHttpRequest", "Target": "GeoService/inFilter", "Interface": "FilterQueryInterface", "Name": "Conn" },
            { "Source": "GeoService/outGeoQuery", "Target": "BOUNDARY/outDbQuery", "Interface": "SqlGeoQueryInterface", "Name": "Conn" },
            { "Source": "HeritageCatalogService/outGeoQuery", "Target": "BOUNDARY/outDbQuery", "Interface": "SqlGeoQueryInterface", "Name": "Conn" },
            { "Source": "BOUNDARY/outFileOps", "Target": "FileService/inFileOps", "Interface": "FileStorageInterface", "Name": "Conn" }
          ],
          "BoundaryPorts": [
            { "Name": "inHttpRequest", "Direction": "Input", "Interface": "HttpRestInterface", "IsBoundary": true },
            { "Name": "outHttpResponse", "Direction": "Output", "Interface": "HttpRestInterface", "IsBoundary": true },
            { "Name": "outDbQuery", "Direction": "Output", "Interface": "SqlGeoQueryInterface", "IsBoundary": true },
            { "Name": "inDbResult", "Direction": "Input", "Interface": "SqlGeoQueryInterface", "IsBoundary": true },
            { "Name": "outCacheOps", "Direction": "Output", "Interface": "CacheInterface", "IsBoundary": true },
            { "Name": "inCacheOps", "Direction": "Input", "Interface": "CacheInterface", "IsBoundary": true },
            { "Name": "outFileOps", "Direction": "Output", "Interface": "FileStorageInterface", "IsBoundary": true }
          ]
        }
      },
      {
        "Name": "PostgreSQL_PostGIS",
        "Type": "Component",
        "Ports": [
          { "Name": "inSql", "Direction": "Input", "Interface": "SqlGeoQueryInterface", "Stereotype": "" },
          { "Name": "outSql", "Direction": "Output", "Interface": "SqlGeoQueryInterface", "Stereotype": "" }
        ],
        "Properties": { "Extensions": ["postgis"] }
      },
      {
        "Name": "RedisCache",
        "Type": "Component",
        "Ports": [
          { "Name": "inCache", "Direction": "Input", "Interface": "CacheInterface", "Stereotype": "" },
          { "Name": "outCache", "Direction": "Output", "Interface": "CacheInterface", "Stereotype": "" }
        ],
        "Properties": {}
      },
      {
        "Name": "YandexMapsAPI",
        "Type": "Component",
        "Ports": [
          { "Name": "inTileReq", "Direction": "Input", "Interface": "MapProviderInterface", "Stereotype": "" },
          { "Name": "outEvents", "Direction": "Output", "Interface": "MapEventsInterface", "Stereotype": "" }
        ],
        "Properties": { "Version": "2.1" }
      }
    ],
    "Connections": [
      { "Source": "WebClientSPA/outApiRequest", "Target": "BackendAPI/inHttpRequest", "Interface": "HttpRestInterface", "Name": "Conn" },
      { "Source": "BackendAPI/outHttpResponse", "Target": "WebClientSPA/inApiResponse", "Interface": "HttpRestInterface", "Name": "Conn" },
      { "Source": "BackendAPI/outDbQuery", "Target": "PostgreSQL_PostGIS/inSql", "Interface": "SqlGeoQueryInterface", "Name": "Conn" },
      { "Source": "PostgreSQL_PostGIS/outSql", "Target": "BackendAPI/inDbResult", "Interface": "SqlGeoQueryInterface", "Name": "Conn" },
      { "Source": "BackendAPI/outCacheOps", "Target": "RedisCache/inCache", "Interface": "CacheInterface", "Name": "Conn" },
      { "Source": "RedisCache/outCache", "Target": "BackendAPI/inCacheOps", "Interface": "CacheInterface", "Name": "Conn" },
      { "Source": "WebClientSPA/outMapTilesReq", "Target": "YandexMapsAPI/inTileReq", "Interface": "MapProviderInterface", "Name": "Conn" },
      { "Source": "YandexMapsAPI/outEvents", "Target": "WebClientSPA/inMapEvents", "Interface": "MapEventsInterface", "Name": "Conn" }
    ],
    "BoundaryPorts": []
  },
  "Interfaces": [
    { "Name": "HttpRestInterface", "Type": "InferredFromPort" },
    { "Name": "SqlGeoQueryInterface", "Type": "InferredFromPort" },
    { "Name": "CacheInterface", "Type": "InferredFromPort" },
    { "Name": "AuthInterface", "Type": "InferredFromPort" },
    { "Name": "CrudInterface", "Type": "InferredFromPort" },
    { "Name": "GeoFeaturesInterface", "Type": "InferredFromPort" },
    { "Name": "FilterQueryInterface", "Type": "InferredFromPort" },
    { "Name": "ViewportInterface", "Type": "InferredFromPort" },
    { "Name": "MapProviderInterface", "Type": "InferredFromPort" },
    { "Name": "MapEventsInterface", "Type": "InferredFromPort" },
    { "Name": "FeatureSelectInterface", "Type": "InferredFromPort" },
    { "Name": "FileStorageInterface", "Type": "InferredFromPort" },
    { "Name": "SearchRequestInterface", "Type": "InferredFromPort" },
    { "Name": "SearchResultInterface", "Type": "InferredFromPort" }
  ],
  "Requirements": [
    {
      "ID": "REQ-001",
      "Name": "Интерактивная карта памятников",
      "Type": "Functional",
      "Priority": "High",
      "ChildIDs": ["REQ-001-1", "REQ-001-2", "REQ-001-3"]
    },
    {
      "ID": "REQ-001-1",
      "Name": "Система должна отображать памятники на карте с маркерами и кластеризацией",
      "Type": "Functional",
      "Priority": "High",
      "ParentID": "REQ-001",
      "ChildIDs": []
    },
    {
      "ID": "REQ-001-2",
      "Name": "Система должна поддерживать переключение слоёв (схема/спутник)",
      "Type": "Functional",
      "Priority": "Medium",
      "ParentID": "REQ-001",
      "ChildIDs": []
    },
    {
      "ID": "REQ-001-3",
      "Name": "Система должна подгружать объекты по текущему окну карты (bbox) для оптимизации",
      "Type": "Functional",
      "Priority": "High",
      "ParentID": "REQ-001",
      "ChildIDs": []
    },
    {
      "ID": "REQ-002",
      "Name": "Фильтрация памятников",
      "Type": "Functional",
      "Priority": "High",
      "ChildIDs": ["REQ-002-1", "REQ-002-2"]
    },
    {
      "ID": "REQ-002-1",
      "Name": "Фильтрация по типу памятника должна выполняться динамически без перезагрузки страницы",
      "Type": "Functional",
      "Priority": "High",
      "ParentID": "REQ-002",
      "ChildIDs": []
    },
    {
      "ID": "REQ-002-2",
      "Name": "Фильтрация по эпохе должна поддерживать множественный выбор",
      "Type": "Functional",
      "Priority": "Medium",
      "ParentID": "REQ-002",
      "ChildIDs": []
    },
    {
      "ID": "REQ-003",
      "Name": "Администрирование (CRUD)",
      "Type": "Functional",
      "Priority": "High",
      "ChildIDs": ["REQ-003-1", "REQ-003-2", "REQ-003-3"]
    },
    {
      "ID": "REQ-003-1",
      "Name": "Администратор должен создавать/редактировать/удалять памятники и справочники",
      "Type": "Functional",
      "Priority": "High",
      "ParentID": "REQ-003",
      "ChildIDs": []
    },
    {
      "ID": "REQ-003-2",
      "Name": "Система должна поддерживать загрузку и привязку документов (PDF) к памятнику",
      "Type": "Functional",
      "Priority": "Medium",
      "ParentID": "REQ-003",
      "ChildIDs": []
    },
    {
      "ID": "REQ-003-3",
      "Name": "Доступ к админ-функциям должен быть ограничен ролями и JWT",
      "Type": "Functional",
      "Priority": "High",
      "ParentID": "REQ-003",
      "ChildIDs": []
    },
    {
      "ID": "REQ-004",
      "Name": "Гео-логика определения административного района",
      "Type": "Functional",
      "Priority": "High",
      "ChildIDs": ["REQ-004-1"]
    },
    {
      "ID": "REQ-004-1",
      "Name": "При добавлении/изменении точки система должна автоматически определять район через PostGIS (ST_Intersects) и сохранять его",
      "Type": "Functional",
      "Priority": "High",
      "ParentID": "REQ-004",
      "ChildIDs": []
    },
    {
      "ID": "REQ-005",
      "Name": "Кэширование запросов",
      "Type": "NonFunctional",
      "Priority": "Medium",
      "ChildIDs": ["REQ-005-1"]
    },
    {
      "ID": "REQ-005-1",
      "Name": "Частые запросы к справочникам и фильтрам должны кэшироваться в Redis с инвалидацией при изменениях",
      "Type": "NonFunctional",
      "Priority": "Medium",
      "ParentID": "REQ-005",
      "ChildIDs": []
    },
    {
      "ID": "REQ-006",
      "Name": "Поиск во внешних источниках по координатам",
      "Type": "Functional",
      "Priority": "Low",
      "ChildIDs": ["REQ-006-1"]
    },
    {
      "ID": "REQ-006-1",
      "Name": "Система должна формировать поисковые запросы/ссылки в Elibrary/Google на основе координат и названия объекта",
      "Type": "Functional",
      "Priority": "Low",
      "ParentID": "REQ-006",
      "ChildIDs": []
    }
  ]
}
```

## 3) Вопрос на уточнение (чтобы сделать «в точку»)
Что именно вам нужно получить на выходе:
1) **исправленный JSON** целиком под вашу веб‑ГИС (как выше, но более детально и строго под ваш формат экспорта),  
2) **UML/SysML диаграммы** (компонентная, развертывания, последовательностей для фильтрации/CRUD),  
3) **ERD/схему БД PostGIS** (таблицы памятников/эпох/типов/районов/документов + индексы GIST),  
4) или **полный набор требований** (functional/non-functional + критерии верификации)?

Скажите вариант(ы) и желаемую детализацию — и я подготовлю финальную версию.