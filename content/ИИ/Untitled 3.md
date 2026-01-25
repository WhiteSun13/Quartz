Тема: Разработка веб-ориентированной геоинформационной системы (ГИС) для археологии.
Суть проекта:
Полнофункциональное веб-приложение (SPA) для сбора, хранения, визуализации и анализа данных об археологических памятниках с географической привязкой. Система решает проблему разрозненности археологических данных и предоставляет инструмент для исследователей.
Технологический стек:
Frontend: Vue.js 3 (Composition API), Naive UI, Vite.
Backend: Node.js, Express.js.
Картография: Yandex Maps API 2.1 (кластеризация, маркеры).
База данных: PostgreSQL с расширением PostGIS (для пространственных запросов и геометрии).
Кэширование: Redis (для оптимизации запросов и фильтров).
Инфраструктура: Docker, Docker Compose, Nginx (reverse proxy).
Ключевой функционал:
Интерактивная карта: Отображение памятников, кластеризация, смена слоев (спутник/схема).
Фильтрация: Динамическая выборка объектов по «Типу памятника» и «Эпохе».
Админ-панель: CRUD-операции для объектов, справочников и прикрепленных документов (PDF). Вход через JWT-авторизацию.
Гео-логика: Автоматическое определение административного района при добавлении точки (триггеры PostGIS ST_Intersects).
Поиск: Интеграция с внешними поисковиками (Elibrary, Google) по географическим координатам.
Архитектура:
Модульная клиент-серверная архитектура, развернутая в контейнерах. Backend реализует RESTful API. ORM Sequelize используется для работы с БД.

{
  "Name": "AdaptiveLearningGame",
  "ExportDate": "10-Jan-2026 17:19:18",
  "MATLABVersion": "9.10.0.1602886 (R2021a)",
  "Structure": {
    "Components": [
      {
        "Name": "DataManagement",
        "Type": "Component",
        "Stereotype": "",
        "Ports": [
          {
            "Name": "inAnalyticsData",
            "Direction": "Input",
            "Interface": "AnalyticsDataInterface",
            "Stereotype": ""
          },
          {
            "Name": "inSaveRequest",
            "Direction": "Input",
            "Interface": "SaveRequestInterface",
            "Stereotype": ""
          },
          {
            "Name": "outGameData",
            "Direction": "Output",
            "Interface": "GameDataInterface",
            "Stereotype": ""
          }
        ],
        "Properties": {},
        "Internals": {
          "Components": [
            {
              "Name": "ConfigurationManager",
              "Type": "Component",
              "Stereotype": "",
              "Ports": [
                {
                  "Name": "inConfigReq ",
                  "Direction": "Input",
                  "Interface": "None",
                  "Stereotype": ""
                },
                {
                  "Name": "outConfig ",
                  "Direction": "Output",
                  "Interface": "None",
                  "Stereotype": ""
                }
              ],
              "Properties": {}
            },
            {
              "Name": "ContentProvider",
              "Type": "Component",
              "Stereotype": "",
              "Ports": [
                {
                  "Name": "inContentReq ",
                  "Direction": "Input",
                  "Interface": "None",
                  "Stereotype": ""
                },
                {
                  "Name": "outContent ",
                  "Direction": "Output",
                  "Interface": "None",
                  "Stereotype": ""
                }
              ],
              "Properties": {}
            },
            {
              "Name": "SaveLoadManager",
              "Type": "Component",
              "Stereotype": "",
              "Ports": [
                {
                  "Name": "inSaveRequest",
                  "Direction": "Input",
                  "Interface": "SaveRequestInterface",
                  "Stereotype": ""
                },
                {
                  "Name": "outGameData",
                  "Direction": "Output",
                  "Interface": "GameDataInterface",
                  "Stereotype": ""
                }
              ],
              "Properties": {}
            }
          ],
          "Connections": [
            {
              "Source": "BOUNDARY/inSaveRequest",
              "Target": "SaveLoadManager/inSaveRequest",
              "Interface": "None",
              "Name": "Conn",
              "Stereotype": ""
            },
            {
              "Source": "SaveLoadManager/outGameData",
              "Target": "BOUNDARY/outGameData",
              "Interface": "None",
              "Name": "Conn",
              "Stereotype": ""
            }
          ],
          "BoundaryPorts": [
            {
              "Name": "inAnalyticsData",
              "Direction": "Input",
              "Interface": "AnalyticsDataInterface",
              "IsBoundary": true
            },
            {
              "Name": "inSaveRequest",
              "Direction": "Input",
              "Interface": "SaveRequestInterface",
              "IsBoundary": true
            },
            {
              "Name": "outGameData",
              "Direction": "Output",
              "Interface": "GameDataInterface",
              "IsBoundary": true
            }
          ]
        }
      },
      {
        "Name": "GameClient",
        "Type": "Component",
        "Stereotype": "",
        "Ports": [
          {
            "Name": "inGameState",
            "Direction": "Input",
            "Interface": "GameStateInterface",
            "Stereotype": ""
          },
          {
            "Name": "inStatistics",
            "Direction": "Input",
            "Interface": "StatisticsInterface",
            "Stereotype": ""
          },
          {
            "Name": "outPlayerAction",
            "Direction": "Output",
            "Interface": "PlayerActionInterface",
            "Stereotype": ""
          }
        ],
        "Properties": {},
        "Internals": {
          "Components": [
            {
              "Name": "InputHandler",
              "Type": "Component",
              "Stereotype": "",
              "Ports": [
                {
                  "Name": "inInput",
                  "Direction": "Input",
                  "Interface": "None",
                  "Stereotype": ""
                },
                {
                  "Name": "outPlayerAction",
                  "Direction": "Output",
                  "Interface": "PlayerActionInterface",
                  "Stereotype": ""
                }
              ],
              "Properties": {}
            },
            {
              "Name": "SceneRenderer",
              "Type": "Component",
              "Stereotype": "",
              "Ports": [
                {
                  "Name": "inGameState",
                  "Direction": "Input",
                  "Interface": "GameStateInterface",
                  "Stereotype": ""
                },
                {
                  "Name": "inRenderCmd",
                  "Direction": "Input",
                  "Interface": "None",
                  "Stereotype": ""
                },
                {
                  "Name": "outVisual",
                  "Direction": "Output",
                  "Interface": "None",
                  "Stereotype": ""
                }
              ],
              "Properties": {}
            },
            {
              "Name": "UserInterfaceModule",
              "Type": "Component",
              "Stereotype": "",
              "Ports": [
                {
                  "Name": "inStatistics",
                  "Direction": "Input",
                  "Interface": "StatisticsInterface",
                  "Stereotype": ""
                },
                {
                  "Name": "outRenderCmd",
                  "Direction": "Output",
                  "Interface": "None",
                  "Stereotype": ""
                }
              ],
              "Properties": {}
            }
          ],
          "Connections": [
            {
              "Source": "BOUNDARY/inGameState",
              "Target": "SceneRenderer/inGameState",
              "Interface": "None",
              "Name": "Conn",
              "Stereotype": ""
            },
            {
              "Source": "BOUNDARY/inStatistics",
              "Target": "UserInterfaceModule/inStatistics",
              "Interface": "None",
              "Name": "Conn",
              "Stereotype": ""
            },
            {
              "Source": "UserInterfaceModule/outRenderCmd",
              "Target": "SceneRenderer/inRenderCmd",
              "Interface": "None",
              "Name": "Conn",
              "Stereotype": ""
            },
            {
              "Source": "InputHandler/outPlayerAction",
              "Target": "BOUNDARY/outPlayerAction",
              "Interface": "None",
              "Name": "Conn",
              "Stereotype": ""
            }
          ],
          "BoundaryPorts": [
            {
              "Name": "inGameState",
              "Direction": "Input",
              "Interface": "GameStateInterface",
              "IsBoundary": true
            },
            {
              "Name": "inStatistics",
              "Direction": "Input",
              "Interface": "StatisticsInterface",
              "IsBoundary": true
            },
            {
              "Name": "outPlayerAction",
              "Direction": "Output",
              "Interface": "PlayerActionInterface",
              "IsBoundary": true
            }
          ]
        }
      },
      {
        "Name": "GameLogicCore",
        "Type": "Component",
        "Stereotype": "",
        "Ports": [
          {
            "Name": "inGameData",
            "Direction": "Input",
            "Interface": "GameDataInterface",
            "Stereotype": ""
          },
          {
            "Name": "inPlayerAction",
            "Direction": "Input",
            "Interface": "PlayerActionInterface",
            "Stereotype": ""
          },
          {
            "Name": "outGameState",
            "Direction": "Output",
            "Interface": "GameStateInterface",
            "Stereotype": ""
          },
          {
            "Name": "outQuestUpdate",
            "Direction": "Output",
            "Interface": "QuestUpdateInterface",
            "Stereotype": ""
          },
          {
            "Name": "outSaveRequest",
            "Direction": "Output",
            "Interface": "SaveRequestInterface",
            "Stereotype": ""
          }
        ],
        "Properties": {},
        "Internals": {
          "Components": [
            {
              "Name": "AIIntegrator",
              "Type": "Component",
              "Stereotype": "",
              "Ports": [
                {
                  "Name": "inDialogContext",
                  "Direction": "Input",
                  "Interface": "None",
                  "Stereotype": ""
                },
                {
                  "Name": "outAIText",
                  "Direction": "Output",
                  "Interface": "None",
                  "Stereotype": ""
                }
              ],
              "Properties": {}
            },
            {
              "Name": "NPCManager",
              "Type": "Component",
              "Stereotype": "",
              "Ports": [
                {
                  "Name": "inPlayerAction",
                  "Direction": "Input",
                  "Interface": "PlayerActionInterface",
                  "Stereotype": ""
                },
                {
                  "Name": "outGameState",
                  "Direction": "Output",
                  "Interface": "GameStateInterface",
                  "Stereotype": ""
                }
              ],
              "Properties": {}
            },
            {
              "Name": "QuestSystem",
              "Type": "Component",
              "Stereotype": "",
              "Ports": [
                {
                  "Name": "inGameData",
                  "Direction": "Input",
                  "Interface": "GameDataInterface",
                  "Stereotype": ""
                },
                {
                  "Name": "outQuestUpdate",
                  "Direction": "Output",
                  "Interface": "QuestUpdateInterface",
                  "Stereotype": ""
                },
                {
                  "Name": "outSaveRequest",
                  "Direction": "Output",
                  "Interface": "SaveRequestInterface",
                  "Stereotype": ""
                }
              ],
              "Properties": {}
            }
          ],
          "Connections": [
            {
              "Source": "BOUNDARY/inPlayerAction",
              "Target": "NPCManager/inPlayerAction",
              "Interface": "None",
              "Name": "Conn",
              "Stereotype": ""
            },
            {
              "Source": "BOUNDARY/inGameData",
              "Target": "QuestSystem/inGameData",
              "Interface": "None",
              "Name": "Conn",
              "Stereotype": ""
            },
            {
              "Source": "NPCManager/outGameState",
              "Target": "BOUNDARY/outGameState",
              "Interface": "None",
              "Name": "Conn",
              "Stereotype": ""
            },
            {
              "Source": "QuestSystem/outQuestUpdate",
              "Target": "BOUNDARY/outQuestUpdate",
              "Interface": "None",
              "Name": "Conn",
              "Stereotype": ""
            },
            {
              "Source": "QuestSystem/outSaveRequest",
              "Target": "BOUNDARY/outSaveRequest",
              "Interface": "None",
              "Name": "Conn",
              "Stereotype": ""
            }
          ],
          "BoundaryPorts": [
            {
              "Name": "inGameData",
              "Direction": "Input",
              "Interface": "GameDataInterface",
              "IsBoundary": true
            },
            {
              "Name": "inPlayerAction",
              "Direction": "Input",
              "Interface": "PlayerActionInterface",
              "IsBoundary": true
            },
            {
              "Name": "outGameState",
              "Direction": "Output",
              "Interface": "GameStateInterface",
              "IsBoundary": true
            },
            {
              "Name": "outQuestUpdate",
              "Direction": "Output",
              "Interface": "QuestUpdateInterface",
              "IsBoundary": true
            },
            {
              "Name": "outSaveRequest",
              "Direction": "Output",
              "Interface": "SaveRequestInterface",
              "IsBoundary": true
            }
          ]
        }
      },
      {
        "Name": "ProgressAnalytics",
        "Type": "Component",
        "Stereotype": "",
        "Ports": [
          {
            "Name": "inQuestUpdate",
            "Direction": "Input",
            "Interface": "QuestUpdateInterface",
            "Stereotype": ""
          },
          {
            "Name": "outAnalyticsData",
            "Direction": "Output",
            "Interface": "AnalyticsDataInterface",
            "Stereotype": ""
          },
          {
            "Name": "outStatistics",
            "Direction": "Output",
            "Interface": "StatisticsInterface",
            "Stereotype": ""
          }
        ],
        "Properties": {},
        "Internals": {
          "Components": [
            {
              "Name": "AchievementSystem",
              "Type": "Component",
              "Stereotype": "",
              "Ports": [
                {
                  "Name": "inStats",
                  "Direction": "Input",
                  "Interface": "None",
                  "Stereotype": ""
                },
                {
                  "Name": "outAchievements ",
                  "Direction": "Output",
                  "Interface": "None",
                  "Stereotype": ""
                }
              ],
              "Properties": {}
            },
            {
              "Name": "ReportGenerator",
              "Type": "Component",
              "Stereotype": "",
              "Ports": [
                {
                  "Name": "inAnalytics",
                  "Direction": "Input",
                  "Interface": "None",
                  "Stereotype": ""
                },
                {
                  "Name": "outReport ",
                  "Direction": "Output",
                  "Interface": "None",
                  "Stereotype": ""
                }
              ],
              "Properties": {}
            },
            {
              "Name": "StatisticsTracker",
              "Type": "Component",
              "Stereotype": "",
              "Ports": [
                {
                  "Name": "inQuestUpdate",
                  "Direction": "Input",
                  "Interface": "QuestUpdateInterface",
                  "Stereotype": ""
                },
                {
                  "Name": "outAnalyticsData",
                  "Direction": "Output",
                  "Interface": "AnalyticsDataInterface",
                  "Stereotype": ""
                },
                {
                  "Name": "outStatistics",
                  "Direction": "Output",
                  "Interface": "StatisticsInterface",
                  "Stereotype": ""
                }
              ],
              "Properties": {}
            }
          ],
          "Connections": [
            {
              "Source": "BOUNDARY/inQuestUpdate",
              "Target": "StatisticsTracker/inQuestUpdate",
              "Interface": "None",
              "Name": "Conn",
              "Stereotype": ""
            },
            {
              "Source": "StatisticsTracker/outAnalyticsData",
              "Target": "BOUNDARY/outAnalyticsData",
              "Interface": "None",
              "Name": "Conn",
              "Stereotype": ""
            },
            {
              "Source": "StatisticsTracker/outStatistics",
              "Target": "BOUNDARY/outStatistics",
              "Interface": "None",
              "Name": "Conn",
              "Stereotype": ""
            }
          ],
          "BoundaryPorts": [
            {
              "Name": "inQuestUpdate",
              "Direction": "Input",
              "Interface": "QuestUpdateInterface",
              "IsBoundary": true
            },
            {
              "Name": "outAnalyticsData",
              "Direction": "Output",
              "Interface": "AnalyticsDataInterface",
              "IsBoundary": true
            },
            {
              "Name": "outStatistics",
              "Direction": "Output",
              "Interface": "StatisticsInterface",
              "IsBoundary": true
            }
          ]
        }
      }
    ],
    "Connections": [
      {
        "Source": "ProgressAnalytics/outAnalyticsData",
        "Target": "DataManagement/inAnalyticsData",
        "Interface": "None",
        "Name": "Conn",
        "Stereotype": ""
      },
      {
        "Source": "GameLogicCore/outGameState",
        "Target": "GameClient/inGameState",
        "Interface": "None",
        "Name": "Conn",
        "Stereotype": ""
      },
      {
        "Source": "GameLogicCore/outQuestUpdate",
        "Target": "ProgressAnalytics/inQuestUpdate",
        "Interface": "None",
        "Name": "Conn",
        "Stereotype": ""
      },
      {
        "Source": "ProgressAnalytics/outStatistics",
        "Target": "GameClient/inStatistics",
        "Interface": "None",
        "Name": "Conn",
        "Stereotype": ""
      },
      {
        "Source": "GameLogicCore/outSaveRequest",
        "Target": "DataManagement/inSaveRequest",
        "Interface": "None",
        "Name": "Conn",
        "Stereotype": ""
      },
      {
        "Source": "DataManagement/outGameData",
        "Target": "GameLogicCore/inGameData",
        "Interface": "None",
        "Name": "Conn",
        "Stereotype": ""
      },
      {
        "Source": "GameClient/outPlayerAction",
        "Target": "GameLogicCore/inPlayerAction",
        "Interface": "None",
        "Name": "Conn",
        "Stereotype": ""
      }
    ],
    "BoundaryPorts": []
  },
  "Interfaces": [
    {
      "Name": "AnalyticsDataInterface",
      "Type": "InferredFromPort"
    },
    {
      "Name": "SaveRequestInterface",
      "Type": "InferredFromPort"
    },
    {
      "Name": "GameDataInterface",
      "Type": "InferredFromPort"
    },
    {
      "Name": "GameStateInterface",
      "Type": "InferredFromPort"
    },
    {
      "Name": "StatisticsInterface",
      "Type": "InferredFromPort"
    },
    {
      "Name": "PlayerActionInterface",
      "Type": "InferredFromPort"
    },
    {
      "Name": "QuestUpdateInterface",
      "Type": "InferredFromPort"
    }
  ],
  "Requirements": [
    {
      "ID": "REQ-001",
      "Name": "Обработка ввода игрока",
      "Description": "",
      "Type": "Functional",
      "Priority": "Medium",
      "Status": "",
      "VerificationStatus": "",
      "Rationale": "",
      "Keywords": [],
      "CustomAttributes": {},
      "LinkedElements": [],
      "ParentID": "",
      "ChildIDs": [
        "REQ-GC-001",
        "REQ-GC-002",
        "REQ-GC-003"
      ]
    },
    {
      "ID": "REQ-002",
      "Name": "Реакция NPC",
      "Description": "",
      "Type": "Functional",
      "Priority": "Medium",
      "Status": "",
      "VerificationStatus": "",
      "Rationale": "",
      "Keywords": [],
      "CustomAttributes": {},
      "LinkedElements": [],
      "ParentID": "",
      "ChildIDs": [
        "REQ-GLC-001"
      ]
    },
    {
      "ID": "REQ-003",
      "Name": "Отслеживание прогресса",
      "Description": "",
      "Type": "Functional",
      "Priority": "Medium",
      "Status": "",
      "VerificationStatus": "",
      "Rationale": "",
      "Keywords": [],
      "CustomAttributes": {},
      "LinkedElements": [],
      "ParentID": "",
      "ChildIDs": [
        "REQ-GLC-002",
        "REQ-GLC-003"
      ]
    },
    {
      "ID": "REQ-004",
      "Name": "Сохранение данных",
      "Description": "",
      "Type": "Functional",
      "Priority": "Medium",
      "Status": "",
      "VerificationStatus": "",
      "Rationale": "",
      "Keywords": [],
      "CustomAttributes": {},
      "LinkedElements": [],
      "ParentID": "",
      "ChildIDs": [
        "REQ-PA-001",
        "REQ-PA-002",
        "REQ-PA-003"
      ]
    },
    {
      "ID": "REQ-005",
      "Name": "Отображение статистики",
      "Description": "",
      "Type": "Functional",
      "Priority": "Medium",
      "Status": "",
      "VerificationStatus": "",
      "Rationale": "",
      "Keywords": [],
      "CustomAttributes": {},
      "LinkedElements": [],
      "ParentID": "",
      "ChildIDs": [
        "REQ-DM-001",
        "REQ-DM-002",
        "REQ-DM-003"
      ]
    },
    {
      "ID": "REQ-GLC-001",
      "Name": "Менеджер должен управлять диалоговыми деревьями и поведением NPC через FSM",
      "Description": "",
      "Type": "Functional",
      "Priority": "Medium",
      "Status": "",
      "VerificationStatus": "",
      "Rationale": "",
      "Keywords": [],
      "CustomAttributes": {},
      "LinkedElements": [],
      "ParentID": "REQ-002",
      "ChildIDs": []
    },
    {
      "ID": "REQ-GC-001",
      "Name": "Модуль должен предоставлять интерфейс для отображения диалогов, заданий, статистики и инструкций",
      "Description": "",
      "Type": "Functional",
      "Priority": "Medium",
      "Status": "",
      "VerificationStatus": "",
      "Rationale": "",
      "Keywords": [],
      "CustomAttributes": {},
      "LinkedElements": [],
      "ParentID": "REQ-001",
      "ChildIDs": []
    },
    {
      "ID": "REQ-GC-002",
      "Name": "Рендерер должен отображать 3D-локации и анимировать персонажей с навигацией по NavMesh",
      "Description": "",
      "Type": "Functional",
      "Priority": "Medium",
      "Status": "",
      "VerificationStatus": "",
      "Rationale": "",
      "Keywords": [],
      "CustomAttributes": {},
      "LinkedElements": [],
      "ParentID": "REQ-001",
      "ChildIDs": []
    },
    {
      "ID": "REQ-GC-003",
      "Name": "Обработчик должен регистрировать ввод с клавиатуры (WASD, 1-3, J/M/I) и мыши",
      "Description": "",
      "Type": "Functional",
      "Priority": "Medium",
      "Status": "",
      "VerificationStatus": "",
      "Rationale": "",
      "Keywords": [],
      "CustomAttributes": {},
      "LinkedElements": [],
      "ParentID": "REQ-001",
      "ChildIDs": []
    },
    {
      "ID": "REQ-GLC-002",
      "Name": "Система должна создавать, отслеживать и оценивать выполнение заданий по времени и точности",
      "Description": "",
      "Type": "Functional",
      "Priority": "Medium",
      "Status": "",
      "VerificationStatus": "",
      "Rationale": "",
      "Keywords": [],
      "CustomAttributes": {},
      "LinkedElements": [],
      "ParentID": "REQ-003",
      "ChildIDs": []
    },
    {
      "ID": "REQ-PA-001",
      "Name": "Трекер должен собирать статистику по времени, квестам и финансовым операциям",
      "Description": "",
      "Type": "Functional",
      "Priority": "Medium",
      "Status": "",
      "VerificationStatus": "",
      "Rationale": "",
      "Keywords": [],
      "CustomAttributes": {},
      "LinkedElements": [],
      "ParentID": "REQ-004",
      "ChildIDs": []
    },
    {
      "ID": "REQ-DM-001",
      "Name": "Менеджер должен сохранять и загружать прогресс игры с созданием резервных копий",
      "Description": "",
      "Type": "Functional",
      "Priority": "Medium",
      "Status": "",
      "VerificationStatus": "",
      "Rationale": "",
      "Keywords": [],
      "CustomAttributes": {},
      "LinkedElements": [],
      "ParentID": "REQ-005",
      "ChildIDs": []
    },
    {
      "ID": "REQ-GLC-003",
      "Name": "Интегратор должен генерировать диалоги через LLM (Ollama) с кэшированием и валидацией",
      "Description": "",
      "Type": "Functional",
      "Priority": "Medium",
      "Status": "",
      "VerificationStatus": "",
      "Rationale": "",
      "Keywords": [],
      "CustomAttributes": {},
      "LinkedElements": [],
      "ParentID": "REQ-003",
      "ChildIDs": []
    },
    {
      "ID": "REQ-PA-002",
      "Name": "Система должна управлять достижениями и уведомлять игрока о прогрессе",
      "Description": "",
      "Type": "Functional",
      "Priority": "Medium",
      "Status": "",
      "VerificationStatus": "",
      "Rationale": "",
      "Keywords": [],
      "CustomAttributes": {},
      "LinkedElements": [],
      "ParentID": "REQ-004",
      "ChildIDs": []
    },
    {
      "ID": "REQ-PA-003",
      "Name": "Генератор должен формировать сводки прогресса и данные для анализа",
      "Description": "",
      "Type": "Functional",
      "Priority": "Medium",
      "Status": "",
      "VerificationStatus": "",
      "Rationale": "",
      "Keywords": [],
      "CustomAttributes": {},
      "LinkedElements": [],
      "ParentID": "REQ-004",
      "ChildIDs": []
    },
    {
      "ID": "REQ-DM-002",
      "Name": "Провайдер должен загружать и кэшировать инструкции с поддержкой локализации",
      "Description": "",
      "Type": "Functional",
      "Priority": "Medium",
      "Status": "",
      "VerificationStatus": "",
      "Rationale": "",
      "Keywords": [],
      "CustomAttributes": {},
      "LinkedElements": [],
      "ParentID": "REQ-005",
      "ChildIDs": []
    },
    {
      "ID": "REQ-DM-003",
      "Name": "Менеджер должен хранить и управлять настройками графики, звука и сложности",
      "Description": "",
      "Type": "Functional",
      "Priority": "Medium",
      "Status": "",
      "VerificationStatus": "",
      "Rationale": "",
      "Keywords": [],
      "CustomAttributes": {},
      "LinkedElements": [],
      "ParentID": "REQ-005",
      "ChildIDs": []
    }
  ]
}