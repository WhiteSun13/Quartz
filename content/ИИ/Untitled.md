# Анализ структурной модели и формирование архитектуры ГИС для археологии

## Обзор исходной модели

Предоставленная JSON-структура описывает архитектуру игрового приложения "AdaptiveLearningGame" с компонентами для управления данными, игровой логики, клиента и аналитики. Необходимо адаптировать эту структуру под веб-ориентированную ГИС для археологии.

---

## Адаптированная архитектура ArchaeoGIS

```json
{
  "Name": "ArchaeoGIS",
  "ExportDate": "2025-01-15",
  "Version": "1.0.0",
  "Structure": {
    "Components": [
      {
        "Name": "DataManagement",
        "Type": "Component",
        "Description": "Управление данными, кэширование, работа с PostgreSQL/PostGIS",
        "Ports": [
          {
            "Name": "inSpatialQuery",
            "Direction": "Input",
            "Interface": "SpatialQueryInterface"
          },
          {
            "Name": "inCRUDRequest",
            "Direction": "Input",
            "Interface": "CRUDRequestInterface"
          },
          {
            "Name": "outGeoData",
            "Direction": "Output",
            "Interface": "GeoDataInterface"
          },
          {
            "Name": "outCacheData",
            "Direction": "Output",
            "Interface": "CacheDataInterface"
          }
        ],
        "Internals": {
          "Components": [
            {
              "Name": "PostgreSQLAdapter",
              "Type": "Component",
              "Ports": [
                {"Name": "inQuery", "Direction": "Input", "Interface": "SQLQueryInterface"},
                {"Name": "outResult", "Direction": "Output", "Interface": "QueryResultInterface"}
              ]
            },
            {
              "Name": "PostGISProcessor",
              "Type": "Component",
              "Ports": [
                {"Name": "inSpatialOp", "Direction": "Input", "Interface": "SpatialOperationInterface"},
                {"Name": "outGeometry", "Direction": "Output", "Interface": "GeometryInterface"}
              ]
            },
            {
              "Name": "RedisCache",
              "Type": "Component",
              "Ports": [
                {"Name": "inCacheReq", "Direction": "Input", "Interface": "CacheRequestInterface"},
                {"Name": "outCachedData", "Direction": "Output", "Interface": "CacheDataInterface"}
              ]
            },
            {
              "Name": "DocumentManager",
              "Type": "Component",
              "Ports": [
                {"Name": "inDocRequest", "Direction": "Input", "Interface": "DocumentRequestInterface"},
                {"Name": "outDocument", "Direction": "Output", "Interface": "DocumentInterface"}
              ]
            }
          ],
          "Connections": [
            {"Source": "BOUNDARY/inSpatialQuery", "Target": "PostGISProcessor/inSpatialOp"},
            {"Source": "BOUNDARY/inCRUDRequest", "Target": "PostgreSQLAdapter/inQuery"},
            {"Source": "PostGISProcessor/outGeometry", "Target": "BOUNDARY/outGeoData"},
            {"Source": "RedisCache/outCachedData", "Target": "BOUNDARY/outCacheData"}
          ]
        }
      },
      {
        "Name": "WebClient",
        "Type": "Component",
        "Description": "Vue.js 3 SPA с Naive UI и картографическим модулем",
        "Ports": [
          {
            "Name": "inMapData",
            "Direction": "Input",
            "Interface": "MapDataInterface"
          },
          {
            "Name": "inFilteredResults",
            "Direction": "Input",
            "Interface": "FilterResultInterface"
          },
          {
            "Name": "outUserAction",
            "Direction": "Output",
            "Interface": "UserActionInterface"
          },
          {
            "Name": "outFilterRequest",
            "Direction": "Output",
            "Interface": "FilterRequestInterface"
          }
        ],
        "Internals": {
          "Components": [
            {
              "Name": "MapModule",
              "Type": "Component",
              "Description": "Yandex Maps API 2.1 интеграция",
              "Ports": [
                {"Name": "inGeoObjects", "Direction": "Input", "Interface": "GeoObjectsInterface"},
                {"Name": "outMapInteraction", "Direction": "Output", "Interface": "MapInteractionInterface"}
              ]
            },
            {
              "Name": "ClusterManager",
              "Type": "Component",
              "Ports": [
                {"Name": "inMarkers", "Direction": "Input", "Interface": "MarkersInterface"},
                {"Name": "outClusters", "Direction": "Output", "Interface": "ClustersInterface"}
              ]
            },
            {
              "Name": "FilterPanel",
              "Type": "Component",
              "Ports": [
                {"Name": "inDictionaries", "Direction": "Input", "Interface": "DictionaryInterface"},
                {"Name": "outFilterCriteria", "Direction": "Output", "Interface": "FilterCriteriaInterface"}
              ]
            },
            {
              "Name": "AdminPanel",
              "Type": "Component",
              "Ports": [
                {"Name": "inAuthStatus", "Direction": "Input", "Interface": "AuthStatusInterface"},
                {"Name": "outCRUDAction", "Direction": "Output", "Interface": "CRUDActionInterface"}
              ]
            },
            {
              "Name": "SearchIntegration",
              "Type": "Component",
              "Ports": [
                {"Name": "inCoordinates", "Direction": "Input", "Interface": "CoordinatesInterface"},
                {"Name": "outExternalSearch", "Direction": "Output", "Interface": "ExternalSearchInterface"}
              ]
            }
          ],
          "Connections": [
            {"Source": "BOUNDARY/inMapData", "Target": "MapModule/inGeoObjects"},
            {"Source": "MapModule/outMapInteraction", "Target": "BOUNDARY/outUserAction"},
            {"Source": "FilterPanel/outFilterCriteria", "Target": "BOUNDARY/outFilterRequest"},
            {"Source": "AdminPanel/outCRUDAction", "Target": "BOUNDARY/outUserAction"}
          ]
        }
      },
      {
        "Name": "APIGateway",
        "Type": "Component",
        "Description": "Express.js RESTful API с JWT авторизацией",
        "Ports": [
          {
            "Name": "inHTTPRequest",
            "Direction": "Input",
            "Interface": "HTTPRequestInterface"
          },
          {
            "Name": "inDBResponse",
            "Direction": "Input",
            "Interface": "DBResponseInterface"
          },
          {
            "Name": "outHTTPResponse",
            "Direction": "Output",
            "Interface": "HTTPResponseInterface"
          },
          {
            "Name": "outDBQuery",
            "Direction": "Output",
            "Interface": "DBQueryInterface"
          }
        ],
        "Internals": {
          "Components": [
            {
              "Name": "AuthController",
              "Type": "Component",
              "Ports": [
                {"Name": "inCredentials", "Direction": "Input", "Interface": "CredentialsInterface"},
                {"Name": "outJWTToken", "Direction": "Output", "Interface": "JWTTokenInterface"}
              ]
            },
            {
              "Name": "SiteController",
              "Type": "Component",
              "Description": "CRUD для археологических памятников",
              "Ports": [
                {"Name": "inSiteRequest", "Direction": "Input", "Interface": "SiteRequestInterface"},
                {"Name": "outSiteResponse", "Direction": "Output", "Interface": "SiteResponseInterface"}
              ]
            },
            {
              "Name": "DictionaryController",
              "Type": "Component",
              "Description": "Управление справочниками (типы, эпохи)",
              "Ports": [
                {"Name": "inDictRequest", "Direction": "Input", "Interface": "DictRequestInterface"},
                {"Name": "outDictResponse", "Direction": "Output", "Interface": "DictResponseInterface"}
              ]
            },
            {
              "Name": "GeoProcessor",
              "Type": "Component",
              "Description": "Обработка пространственных запросов",
              "Ports": [
                {"Name": "inGeoRequest", "Direction": "Input", "Interface": "GeoRequestInterface"},
                {"Name": "outGeoResponse", "Direction": "Output", "Interface": "GeoResponseInterface"}
              ]
            },
            {
              "Name": "SequelizeORM",
              "Type": "Component",
              "Ports": [
                {"Name": "inModelQuery", "Direction": "Input", "Interface": "ModelQueryInterface"},
                {"Name": "outModelResult", "Direction": "Output", "Interface": "ModelResultInterface"}
              ]
            }
          ],
          "Connections": [
            {"Source": "BOUNDARY/inHTTPRequest", "Target": "AuthController/inCredentials"},
            {"Source": "SiteController/outSiteResponse", "Target": "BOUNDARY/outHTTPResponse"},
            {"Source": "GeoProcessor/outGeoResponse", "Target": "BOUNDARY/outDBQuery"}
          ]
        }
      },
      {
        "Name": "SpatialAnalytics",
        "Type": "Component",
        "Description": "Пространственный анализ и автоопределение районов",
        "Ports": [
          {
            "Name": "inPointCoordinates",
            "Direction": "Input",
            "Interface": "PointCoordinatesInterface"
          },
          {
            "Name": "inBoundaryData",
            "Direction": "Input",
            "Interface": "BoundaryDataInterface"
          },
          {
            "Name": "outDistrictInfo",
            "Direction": "Output",
            "Interface": "DistrictInfoInterface"
          },
          {
            "Name": "outSpatialResult",
            "Direction": "Output",
            "Interface": "SpatialResultInterface"
          }
        ],
        "Internals": {
          "Components": [
            {
              "Name": "DistrictResolver",
              "Type": "Component",
              "Description": "ST_Intersects для определения района",
              "Ports": [
                {"Name": "inPoint", "Direction": "Input", "Interface": "PointInterface"},
                {"Name": "outDistrict", "Direction": "Output", "Interface": "DistrictInterface"}
              ]
            },
            {
              "Name": "BoundingBoxFilter",
              "Type": "Component",
              "Ports": [
                {"Name": "inViewport", "Direction": "Input", "Interface": "ViewportInterface"},
                {"Name": "outFilteredSites", "Direction": "Output", "Interface": "FilteredSitesInterface"}
              ]
            },
            {
              "Name": "CoordinateValidator",
              "Type": "Component",
              "Ports": [
                {"Name": "inRawCoords", "Direction": "Input", "Interface": "RawCoordsInterface"},
                {"Name": "outValidCoords", "Direction": "Output", "Interface": "ValidCoordsInterface"}
              ]
            }
          ],
          "Connections": [
            {"Source": "BOUNDARY/inPointCoordinates", "Target": "CoordinateValidator/inRawCoords"},
            {"Source": "CoordinateValidator/outValidCoords", "Target": "DistrictResolver/inPoint"},
            {"Source": "DistrictResolver/outDistrict", "Target": "BOUNDARY/outDistrictInfo"}
          ]
        }
      }
    ],
    "Connections": [
      {
        "Source": "WebClient/outUserAction",
        "Target": "APIGateway/inHTTPRequest",
        "Interface": "HTTPRequestInterface",
        "Name": "UserRequestFlow"
      },
      {
        "Source": "WebClient/outFilterRequest",
        "Target": "APIGateway/inHTTPRequest",
        "Interface": "FilterRequestInterface",
        "Name": "FilterFlow"
      },
      {
        "Source": "APIGateway/outDBQuery",
        "Target": "DataManagement/inSpatialQuery",
        "Interface": "SpatialQueryInterface",
        "Name": "SpatialQueryFlow"
      },
      {
        "Source": "APIGateway/outDBQuery",
        "Target": "DataManagement/inCRUDRequest",
        "Interface": "CRUDRequestInterface",
        "Name": "CRUDFlow"
      },
      {
        "Source": "DataManagement/outGeoData",
        "Target": "APIGateway/inDBResponse",
        "Interface": "GeoDataInterface",
        "Name": "GeoDataFlow"
      },
      {
        "Source": "APIGateway/outHTTPResponse",
        "Target": "WebClient/inMapData",
        "Interface": "MapDataInterface",
        "Name": "MapDataFlow"
      },
      {
        "Source": "DataManagement/outGeoData",
        "Target": "SpatialAnalytics/inPointCoordinates",
        "Interface": "PointCoordinatesInterface",
        "Name": "SpatialAnalysisFlow"
      },
      {
        "Source": "SpatialAnalytics/outDistrictInfo",
        "Target": "DataManagement/inCRUDRequest",
        "Interface": "DistrictUpdateInterface",
        "Name": "DistrictUpdateFlow"
      }
    ]
  },
  "Interfaces": [
    {"Name": "SpatialQueryInterface", "Type": "Data", "Description": "Пространственные запросы PostGIS"},
    {"Name": "CRUDRequestInterface", "Type": "Data", "Description": "CRUD операции с памятниками"},
    {"Name": "GeoDataInterface", "Type": "Data", "Description": "Геоданные с координатами"},
    {"Name": "CacheDataInterface", "Type": "Data", "Description": "Кэшированные данные Redis"},
    {"Name": "MapDataInterface", "Type": "Data", "Description": "Данные для отображения на карте"},
    {"Name": "FilterResultInterface", "Type": "Data", "Description": "Результаты фильтрации"},
    {"Name": "UserActionInterface", "Type": "Event", "Description": "Действия пользователя"},
    {"Name": "FilterRequestInterface", "Type": "Data", "Description": "Запрос фильтрации"},
    {"Name": "HTTPRequestInterface", "Type": "Protocol", "Description": "HTTP запросы REST API"},
    {"Name": "HTTPResponseInterface", "Type": "Protocol", "Description": "HTTP ответы REST API"},
    {"Name": "JWTTokenInterface", "Type": "Security", "Description": "JWT токены авторизации"},
    {"Name": "PointCoordinatesInterface", "Type": "Data", "Description": "Координаты точки"},
    {"Name": "DistrictInfoInterface", "Type": "Data", "Description": "Информация о районе"}
  ],
  "Requirements": [
    {
      "ID": "REQ-001",
      "Name": "Интерактивная карта",
      "Description": "Отображение археологических памятников на карте",
      "Type": "Functional",
      "Priority": "High",
      "ChildIDs": ["REQ-MAP-001", "REQ-MAP-002", "REQ-MAP-003"]
    },
    {
      "ID": "REQ-MAP-001",
      "Name": "Отображение маркеров памятников с кластеризацией",
      "Type": "Functional",
      "Priority": "High",
      "ParentID": "REQ-001",
      "LinkedElements": ["WebClient/MapModule", "WebClient/ClusterManager"]
    },
    {
      "ID": "REQ-MAP-002",
      "Name": "Переключение слоёв карты (спутник/схема)",
      "Type": "Functional",
      "Priority": "Medium",
      "ParentID": "REQ-001",
      "LinkedElements": ["WebClient/MapModule"]
    },
    {
      "ID": "REQ-MAP-003",
      "Name": "Интеграция с Yandex Maps API 2.1",
      "Type": "Technical",
      "Priority": "High",
      "ParentID": "REQ-001",
      "LinkedElements": ["WebClient/MapModule"]
    },
    {
      "ID": "REQ-002",
      "Name": "Фильтрация данных",
      "Description": "Динамическая фильтрация объектов",
      "Type": "Functional",
      "Priority": "High",
      "ChildIDs": ["REQ-FLT-001", "REQ-FLT-002"]
    },
    {
      "ID": "REQ-FLT-001",
      "Name": "Фильтрация по типу памятника",
      "Type": "Functional",
      "Priority": "High",
      "ParentID": "REQ-002",
      "LinkedElements": ["WebClient/FilterPanel", "APIGateway/DictionaryController"]
    },
    {
      "ID": "REQ-FLT-002",
      "Name": "Фильтрация по эпохе",
      "Type": "Functional",
      "Priority": "High",
      "ParentID": "REQ-002",
      "LinkedElements": ["WebClient/FilterPanel", "DataManagement/RedisCache"]
    },
    {
      "ID": "REQ-003",
      "Name": "Админ-панель",
      "Description": "Административное управление данными",
      "Type": "Functional",
      "Priority": "High",
      "ChildIDs": ["REQ-ADM-001", "REQ-ADM-002", "REQ-ADM-003", "REQ-ADM-004"]
    },
    {
      "ID": "REQ-ADM-001",
      "Name": "CRUD операции для памятников",
      "Type": "Functional",
      "Priority": "High",
      "ParentID": "REQ-003",
      "LinkedElements": ["WebClient/AdminPanel", "APIGateway/SiteController"]
    },
    {
      "ID": "REQ-ADM-002",
      "Name": "Управление справочниками",
      "Type": "Functional",
      "Priority": "Medium",
      "ParentID": "REQ-003",
      "LinkedElements": ["APIGateway/DictionaryController"]
    },
    {
      "ID": "REQ-ADM-003",
      "Name": "Прикрепление PDF документов",
      "Type": "Functional",
      "Priority": "Medium",
      "ParentID": "REQ-003",
      "LinkedElements": ["DataManagement/DocumentManager"]
    },
    {
      "ID": "REQ-ADM-004",
      "Name": "JWT авторизация администратора",
      "Type": "Security",
      "Priority": "Critical",
      "ParentID": "REQ-003",
      "LinkedElements": ["APIGateway/AuthController"]
    },
    {
      "ID": "REQ-004",
      "Name": "Гео-логика",
      "Description": "Автоматическая обработка геоданных",
      "Type": "Functional",
      "Priority": "High",
      "ChildIDs": ["REQ-GEO-001", "REQ-GEO-002"]
    },
    {
      "ID": "REQ-GEO-001",
      "Name": "Автоопределение района по координатам (ST_Intersects)",
      "Type": "Functional",
      "Priority": "High",
      "ParentID": "REQ-004",
      "LinkedElements": ["SpatialAnalytics/DistrictResolver", "DataManagement/PostGISProcessor"]
    },
    {
      "ID": "REQ-GEO-002",
      "Name": "Валидация координат",
      "Type": "Functional",
      "Priority": "Medium",
      "ParentID": "REQ-004",
      "LinkedElements": ["SpatialAnalytics/CoordinateValidator"]
    },
    {
      "ID": "REQ-005",
      "Name": "Интеграция с внешними поисковиками",
      "Description": "Поиск по Elibrary и Google Scholar",
      "Type": "Functional",
      "Priority": "Low",
      "LinkedElements": ["WebClient/SearchIntegration"]
    },
    {
      "ID": "REQ-006",
      "Name": "Инфраструктура",
      "Description": "Контейнеризация и развертывание",
      "Type": "NonFunctional",
      "Priority": "High",
      "ChildIDs": ["REQ-INF-001", "REQ-INF-002", "REQ-INF-003"]
    },
    {
      "ID": "REQ-INF-001",
      "Name": "Docker контейнеризация всех сервисов",
      "Type": "Technical",
      "Priority": "High",
      "ParentID": "REQ-006"
    },
    {
      "ID": "REQ-INF-002",
      "Name": "Docker Compose оркестрация",
      "Type": "Technical",
      "Priority": "High",
      "ParentID": "REQ-006"
    },
    {
      "ID": "REQ-INF-003",
      "Name": "Nginx reverse proxy",
      "Type": "Technical",
      "Priority": "Medium",
      "ParentID": "REQ-006"
    }
  ]
}
```

---

## Диаграмма архитектуры

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              ArchaeoGIS System                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │                         WebClient (Vue.js 3 SPA)                       │ │
│  │  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌───────────────┐  │ │
│  │  │  MapModule   │ │ClusterManager│ │ FilterPanel  │ │  AdminPanel   │  │ │
│  │  │ (Yandex API) │ │              │ │ (Тип/Эпоха)  │ │ (CRUD + JWT)  │  │ │
│  │  └──────┬───────┘ └──────┬───────┘ └──────┬───────┘ └───────┬───────┘  │ │
│  │         │                │                │                 │          │ │
│  │  ┌──────┴────────────────┴────────────────┴─────────────────┴───────┐  │ │
│  │  │                    SearchIntegration (Elibrary/Google)           │  │ │
│  │  └──────────────────────────────────────────────────────────────────┘  │ │
│  └────────────────────────────────┬───────────────────────────────────────┘ │
│                                   │ HTTP/REST                                │
│                                   ▼                                          │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │                      APIGateway (Express.js)                           │ │
│  │  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌───────────────┐  │ │
│  │  │AuthController│ │SiteController│ │  DictCtrl    │ │ GeoProcessor  │  │ │
│  │  │   (JWT)      │ │   (CRUD)     │ │(Справочники) │ │ (PostGIS)     │  │ │
│  │  └──────────────┘ └──────────────┘ └──────────────┘ └───────────────┘  │ │
│  │                          │                                             │ │
│  │  ┌───────────────────────┴─────────────────────────────────────────┐   │ │
│  │  │                      SequelizeORM                                │   │ │
│  │  └──────────────────────────────────────────────────────────────────┘   │ │
│  └────────────────────────────────┬───────────────────────────────────────┘ │
│                                   │ SQL/PostGIS                              │
│           ┌───────────────────────┼───────────────────────┐                  │
│           ▼                       ▼                       ▼                  │
│  ┌─────────────────┐  ┌─────────────────────┐  ┌─────────────────────────┐  │
│  │  DataManagement │  │  SpatialAnalytics   │  │       Redis Cache       │  │
│  │  ┌───────────┐  │  │  ┌───────────────┐  │  │  ┌─────────────────┐    │  │
│  │  │PostgreSQL │  │  │  │DistrictResolv │  │  │  │ Фильтры/Справ.  │    │  │
│  │  │ + PostGIS │  │  │  │(ST_Intersects)│  │  │  │     Cache       │    │  │
│  │  └───────────┘  │  │  └───────────────┘  │  │  └─────────────────┘    │  │
│  │  ┌───────────┐  │  │  ┌───────────────┐  │  └─────────────────────────┘  │
│  │  │ Document  │  │  │  │  BBoxFilter   │  │                               │
│  │  │ Manager   │  │  │  │  Validator    │  │                               │
│  │  └───────────┘  │  │  └───────────────┘  │                               │
│  └─────────────────┘  └─────────────────────┘                               │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘

                    ┌─────────────────────────────────┐
                    │     Infrastructure (Docker)     │
                    │  ┌─────┐ ┌─────┐ ┌─────┐ ┌────┐ │
                    │  │Nginx│ │ App │ │ DB  │ │Redis│ │
                    │  └─────┘ └─────┘ └─────┘ └────┘ │
                    └─────────────────────────────────┘
```

---

## Сопоставление компонентов

| Исходный компонент | Адаптированный компонент | Назначение в ГИС |
|---|---|---|
| GameClient | WebClient | Vue.js SPA с картой и фильтрами |
| GameLogicCore | APIGateway | REST API и бизнес-логика |
| DataManagement | DataManagement | PostgreSQL/PostGIS + Redis |
| ProgressAnalytics | SpatialAnalytics | Пространственный анализ |
| InputHandler | MapModule | Взаимодействие с картой |
| NPCManager | GeoProcessor | Обработка геоданных |
| SaveLoadManager | DocumentManager | Управление PDF документами |
| StatisticsTracker | DistrictResolver | Автоопределение районов |

---

## Ключевые технические решения

### 1. Триггер PostGIS для автоопределения района

```sql
CREATE OR REPLACE FUNCTION determine_district()
RETURNS TRIGGER AS $$
BEGIN
    SELECT d.id, d.name INTO NEW.district_id, NEW.district_name
    FROM districts d
    WHERE ST_Intersects(d.geometry, NEW.location);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_determine_district
BEFORE INSERT OR UPDATE ON archaeological_sites
FOR EACH ROW EXECUTE FUNCTION determine_district();
```

### 2. Структура Redis кэширования

```
archaeo:filters:types     → SET типов памятников
archaeo:filters:epochs    → SET эпох
archaeo:sites:bbox:{hash} → Кэш результатов по viewport
archaeo:site:{id}         → Кэш отдельного памятника
```