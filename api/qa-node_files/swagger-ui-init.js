
window.onload = function() {
  // Build a system
  let url = window.location.search.match(/url=([^&]+)/);
  if (url && url.length > 1) {
    url = decodeURIComponent(url[1]);
  } else {
    url = window.location.origin;
  }
  let options = {
  "swaggerDoc": {
    "openapi": "3.0.0",
    "paths": {
      "/api/v1/user/login": {
        "post": {
          "operationId": "UserController_login",
          "summary": "登录 •【Public】🔑",
          "parameters": [],
          "requestBody": {
            "required": true,
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/UserLoginDto"
                }
              }
            }
          },
          "responses": {
            "200": {
              "description": "",
              "content": {
                "application/json": {
                  "schema": {
                    "allOf": [
                      {
                        "$ref": "#/components/schemas/ResponseDto"
                      },
                      {
                        "properties": {
                          "data": {
                            "$ref": "#/components/schemas/UserDetailDto"
                          }
                        }
                      }
                    ]
                  }
                }
              }
            }
          },
          "tags": [
            "用户"
          ]
        }
      },
      "/api/v1/user/logout": {
        "get": {
          "operationId": "UserController_logout",
          "summary": "退出 •【Public】🔑",
          "parameters": [],
          "responses": {
            "200": {
              "description": "",
              "content": {
                "application/json": {
                  "schema": {
                    "allOf": [
                      {
                        "$ref": "#/components/schemas/ResponseDto"
                      },
                      {
                        "properties": {
                          "data": {
                            "type": "boolean"
                          }
                        }
                      }
                    ]
                  }
                }
              }
            }
          },
          "tags": [
            "用户"
          ]
        }
      },
      "/api/v1/user/register": {
        "post": {
          "operationId": "UserController_register",
          "summary": "账号密码注册 •【Admin】🔐",
          "parameters": [],
          "requestBody": {
            "required": true,
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/UserRegisterDto"
                }
              }
            }
          },
          "responses": {
            "200": {
              "description": "",
              "content": {
                "application/json": {
                  "schema": {
                    "allOf": [
                      {
                        "$ref": "#/components/schemas/ResponseDto"
                      },
                      {
                        "properties": {
                          "data": {
                            "$ref": "#/components/schemas/UserDetailDto"
                          }
                        }
                      }
                    ]
                  }
                }
              }
            }
          },
          "tags": [
            "用户"
          ]
        }
      },
      "/api/v1/user/update/password": {
        "post": {
          "operationId": "UserController_updatePassword",
          "summary": "修改密码",
          "parameters": [],
          "requestBody": {
            "required": true,
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/UserUpdatePassword"
                }
              }
            }
          },
          "responses": {
            "200": {
              "description": "",
              "content": {
                "application/json": {
                  "schema": {
                    "allOf": [
                      {
                        "$ref": "#/components/schemas/ResponseDto"
                      },
                      {
                        "properties": {
                          "data": {
                            "$ref": "#/components/schemas/UserDetailDto"
                          }
                        }
                      }
                    ]
                  }
                }
              }
            }
          },
          "tags": [
            "用户"
          ]
        }
      },
      "/api/v1/user/update/key/info": {
        "post": {
          "operationId": "UserController_updateKeyInfo",
          "summary": "修改用户关键信息 •【Admin】🔐",
          "parameters": [],
          "requestBody": {
            "required": true,
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/UpdateUserKeyInfoDto"
                }
              }
            }
          },
          "responses": {
            "200": {
              "description": "",
              "content": {
                "application/json": {
                  "schema": {
                    "allOf": [
                      {
                        "$ref": "#/components/schemas/ResponseDto"
                      },
                      {
                        "properties": {
                          "data": {
                            "$ref": "#/components/schemas/UserDetailDto"
                          }
                        }
                      }
                    ]
                  }
                }
              }
            }
          },
          "tags": [
            "用户"
          ]
        }
      },
      "/api/v1/user/update/info": {
        "post": {
          "operationId": "UserController_updateInfo",
          "summary": "修改个人信息",
          "parameters": [],
          "requestBody": {
            "required": true,
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/UpdateUserInfoDto"
                }
              }
            }
          },
          "responses": {
            "200": {
              "description": "",
              "content": {
                "application/json": {
                  "schema": {
                    "allOf": [
                      {
                        "$ref": "#/components/schemas/ResponseDto"
                      },
                      {
                        "properties": {
                          "data": {
                            "$ref": "#/components/schemas/UserDetailDto"
                          }
                        }
                      }
                    ]
                  }
                }
              }
            }
          },
          "tags": [
            "用户"
          ]
        }
      },
      "/api/v1/user/avatar/upload": {
        "post": {
          "operationId": "UserController_avatarUpload",
          "summary": "修改个人头像",
          "parameters": [],
          "requestBody": {
            "required": true,
            "content": {
              "application/octet-stream": {
                "schema": {
                  "format": "binary"
                }
              }
            }
          },
          "responses": {
            "200": {
              "description": "",
              "content": {
                "application/json": {
                  "schema": {
                    "allOf": [
                      {
                        "$ref": "#/components/schemas/ResponseDto"
                      },
                      {
                        "properties": {
                          "data": {
                            "type": "string"
                          }
                        }
                      }
                    ]
                  }
                }
              }
            }
          },
          "tags": [
            "用户"
          ]
        }
      },
      "/api/v1/user/info": {
        "get": {
          "operationId": "UserController_detail",
          "summary": "用户信息",
          "parameters": [],
          "responses": {
            "200": {
              "description": "",
              "content": {
                "application/json": {
                  "schema": {
                    "allOf": [
                      {
                        "$ref": "#/components/schemas/ResponseDto"
                      },
                      {
                        "properties": {
                          "data": {
                            "$ref": "#/components/schemas/UserDetailDto"
                          }
                        }
                      }
                    ]
                  }
                }
              }
            }
          },
          "tags": [
            "用户"
          ]
        }
      },
      "/api/v1/user/list": {
        "get": {
          "operationId": "UserController_list",
          "summary": "用户列表 •【Admin】🔐",
          "parameters": [],
          "responses": {
            "200": {
              "description": "",
              "content": {
                "application/json": {
                  "schema": {
                    "allOf": [
                      {
                        "$ref": "#/components/schemas/ResponseDto"
                      },
                      {
                        "properties": {
                          "data": {
                            "type": "array",
                            "items": {
                              "$ref": "#/components/schemas/UserDetailDto"
                            }
                          }
                        }
                      }
                    ]
                  }
                }
              }
            }
          },
          "tags": [
            "用户"
          ]
        }
      },
      "/api/v1/user/listByPage": {
        "post": {
          "operationId": "UserController_listByPage",
          "summary": "用户列表（分页） •【Admin】🔐",
          "parameters": [],
          "requestBody": {
            "required": false,
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/SearchUserInfoDto"
                }
              }
            }
          },
          "responses": {
            "200": {
              "description": "",
              "content": {
                "application/json": {
                  "schema": {
                    "allOf": [
                      {
                        "$ref": "#/components/schemas/ResponseDto"
                      },
                      {
                        "properties": {
                          "data": {
                            "type": "array",
                            "items": {
                              "$ref": "#/components/schemas/UserDetailDto"
                            }
                          }
                        }
                      }
                    ]
                  }
                }
              }
            }
          },
          "tags": [
            "用户"
          ]
        }
      },
      "/api/v1/library/add": {
        "post": {
          "operationId": "LibraryController_create",
          "summary": "创建知识库 •【Admin】🔐",
          "parameters": [],
          "requestBody": {
            "required": true,
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/CreateLibraryDto"
                }
              }
            }
          },
          "responses": {
            "200": {
              "description": "",
              "content": {
                "application/json": {
                  "schema": {
                    "allOf": [
                      {
                        "$ref": "#/components/schemas/ResponseDto"
                      },
                      {
                        "properties": {
                          "data": {
                            "$ref": "#/components/schemas/LibraryDetailDto"
                          }
                        }
                      }
                    ]
                  }
                }
              }
            }
          },
          "tags": [
            "知识库"
          ]
        }
      },
      "/api/v1/library/update": {
        "post": {
          "operationId": "LibraryController_update",
          "summary": "修改知识库 •【Admin】🔐",
          "parameters": [],
          "requestBody": {
            "required": true,
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/UpdateLibraryDto"
                }
              }
            }
          },
          "responses": {
            "200": {
              "description": "",
              "content": {
                "application/json": {
                  "schema": {
                    "allOf": [
                      {
                        "$ref": "#/components/schemas/ResponseDto"
                      },
                      {
                        "properties": {
                          "data": {
                            "$ref": "#/components/schemas/LibraryDetailDto"
                          }
                        }
                      }
                    ]
                  }
                }
              }
            }
          },
          "tags": [
            "知识库"
          ]
        }
      },
      "/api/v1/library/delete": {
        "post": {
          "operationId": "LibraryController_delete",
          "summary": "删除知识库 •【Admin】🔐",
          "parameters": [],
          "requestBody": {
            "required": true,
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/LibraryDeleteDto"
                }
              }
            }
          },
          "responses": {
            "200": {
              "description": "",
              "content": {
                "application/json": {
                  "schema": {
                    "allOf": [
                      {
                        "$ref": "#/components/schemas/ResponseDto"
                      },
                      {
                        "properties": {
                          "data": {
                            "type": "boolean"
                          }
                        }
                      }
                    ]
                  }
                }
              }
            }
          },
          "tags": [
            "知识库"
          ]
        }
      },
      "/api/v1/library/list": {
        "get": {
          "operationId": "LibraryController_list",
          "summary": "知识库列表 •【Public】🔑",
          "parameters": [
            {
              "name": "sort",
              "required": false,
              "in": "query",
              "description": "排序",
              "schema": {
                "enum": [
                  "recentUpdate",
                  "recentUsed",
                  "createTime",
                  "name"
                ],
                "type": "string"
              }
            },
            {
              "name": "sortType",
              "required": false,
              "in": "query",
              "description": "升序/降序",
              "schema": {
                "enum": [
                  "ASC",
                  "DESC"
                ],
                "type": "string"
              }
            },
            {
              "name": "type",
              "required": false,
              "in": "query",
              "description": "知识库类型（自定义知识库10）",
              "schema": {
                "enum": [
                  0,
                  10
                ],
                "type": "number"
              }
            }
          ],
          "responses": {
            "200": {
              "description": "",
              "content": {
                "application/json": {
                  "schema": {
                    "allOf": [
                      {
                        "$ref": "#/components/schemas/ResponseDto"
                      },
                      {
                        "properties": {
                          "data": {
                            "type": "array",
                            "items": {
                              "$ref": "#/components/schemas/LibraryDetailDto"
                            }
                          }
                        }
                      }
                    ]
                  }
                }
              }
            }
          },
          "tags": [
            "知识库"
          ]
        }
      },
      "/api/v1/library/data/tree": {
        "post": {
          "operationId": "LibraryController_dataTree",
          "summary": "自定义知识库树形结构数据",
          "parameters": [],
          "requestBody": {
            "required": true,
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/LibraryTreeDto"
                }
              }
            }
          },
          "responses": {
            "201": {
              "description": ""
            }
          },
          "tags": [
            "知识库"
          ]
        }
      },
      "/api/v1/folder/add": {
        "post": {
          "operationId": "FolderController_create",
          "summary": "创建文件夹",
          "parameters": [],
          "requestBody": {
            "required": true,
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/CreateFolderDto"
                }
              }
            }
          },
          "responses": {
            "200": {
              "description": "",
              "content": {
                "application/json": {
                  "schema": {
                    "allOf": [
                      {
                        "$ref": "#/components/schemas/ResponseDto"
                      },
                      {
                        "properties": {
                          "data": {
                            "$ref": "#/components/schemas/FolderDetailDto"
                          }
                        }
                      }
                    ]
                  }
                }
              }
            }
          },
          "tags": [
            "文件夹"
          ]
        }
      },
      "/api/v1/folder/update": {
        "post": {
          "operationId": "FolderController_update",
          "summary": "编辑文件夹",
          "parameters": [],
          "requestBody": {
            "required": true,
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/UpdateFolderDto"
                }
              }
            }
          },
          "responses": {
            "200": {
              "description": "",
              "content": {
                "application/json": {
                  "schema": {
                    "allOf": [
                      {
                        "$ref": "#/components/schemas/ResponseDto"
                      },
                      {
                        "properties": {
                          "data": {
                            "$ref": "#/components/schemas/FolderDetailDto"
                          }
                        }
                      }
                    ]
                  }
                }
              }
            }
          },
          "tags": [
            "文件夹"
          ]
        }
      },
      "/api/v1/folder/delete": {
        "post": {
          "operationId": "FolderController_delete",
          "summary": "删除文件夹",
          "parameters": [],
          "requestBody": {
            "required": true,
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/FolderDeleteDto"
                }
              }
            }
          },
          "responses": {
            "200": {
              "description": "",
              "content": {
                "application/json": {
                  "schema": {
                    "allOf": [
                      {
                        "$ref": "#/components/schemas/ResponseDto"
                      },
                      {
                        "properties": {
                          "data": {
                            "type": "boolean"
                          }
                        }
                      }
                    ]
                  }
                }
              }
            }
          },
          "tags": [
            "文件夹"
          ]
        }
      },
      "/api/v1/folder/admin/delete": {
        "post": {
          "operationId": "FolderController_deleteByAdmin",
          "parameters": [],
          "responses": {
            "201": {
              "description": ""
            }
          },
          "tags": [
            "文件夹"
          ]
        }
      },
      "/api/v1/folder/move": {
        "post": {
          "operationId": "FolderController_move",
          "summary": "移动文件夹位置",
          "parameters": [],
          "requestBody": {
            "required": true,
            "content": {
              "application/json": {
                "schema": {
                  "type": "array",
                  "items": {
                    "$ref": "#/components/schemas/MoveFolderDto"
                  }
                }
              }
            }
          },
          "responses": {
            "200": {
              "description": "",
              "content": {
                "application/json": {
                  "schema": {
                    "allOf": [
                      {
                        "$ref": "#/components/schemas/ResponseDto"
                      },
                      {
                        "properties": {
                          "data": {
                            "type": "boolean"
                          }
                        }
                      }
                    ]
                  }
                }
              }
            }
          },
          "tags": [
            "文件夹"
          ]
        }
      },
      "/api/v1/folder/data/children": {
        "post": {
          "operationId": "FolderController_dataChildren",
          "summary": "查询文件夹children",
          "parameters": [],
          "requestBody": {
            "required": true,
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/ChildrenQueryDto"
                }
              }
            }
          },
          "responses": {
            "201": {
              "description": ""
            }
          },
          "tags": [
            "文件夹"
          ]
        }
      },
      "/api/v1/document/finance/upload": {
        "post": {
          "operationId": "DocumentController_createFiance",
          "summary": "创建财报知识库文档 •【Admin】🔐",
          "parameters": [
            {
              "name": "noParse",
              "required": true,
              "in": "query",
              "description": "不自动解析文档",
              "schema": {
                "type": "boolean"
              }
            }
          ],
          "requestBody": {
            "required": true,
            "content": {
              "multipart/form-data": {
                "schema": {
                  "$ref": "#/components/schemas/CreateFianceDocumentDto"
                }
              }
            }
          },
          "responses": {
            "200": {
              "description": "",
              "content": {
                "application/json": {
                  "schema": {
                    "allOf": [
                      {
                        "$ref": "#/components/schemas/ResponseDto"
                      },
                      {
                        "properties": {
                          "data": {
                            "$ref": "#/components/schemas/DocumentDto"
                          }
                        }
                      }
                    ]
                  }
                }
              }
            }
          },
          "tags": [
            "文档"
          ]
        }
      },
      "/api/v1/document/upload": {
        "post": {
          "operationId": "DocumentController_upload",
          "summary": "上传自定义知识库文档",
          "parameters": [
            {
              "name": "folderId",
              "required": false,
              "in": "query",
              "description": "文件夹id",
              "schema": {
                "type": "number"
              }
            },
            {
              "name": "filename",
              "required": true,
              "in": "query",
              "description": "文件名",
              "schema": {
                "type": "string"
              }
            },
            {
              "name": "noParse",
              "required": true,
              "in": "query",
              "description": "不自动解析文档",
              "schema": {
                "type": "boolean"
              }
            }
          ],
          "requestBody": {
            "required": true,
            "content": {
              "application/octet-stream": {
                "schema": {
                  "format": "binary"
                }
              }
            }
          },
          "responses": {
            "200": {
              "description": "",
              "content": {
                "application/json": {
                  "schema": {
                    "allOf": [
                      {
                        "$ref": "#/components/schemas/ResponseDto"
                      },
                      {
                        "properties": {
                          "data": {
                            "$ref": "#/components/schemas/DocumentDto"
                          }
                        }
                      }
                    ]
                  }
                }
              }
            }
          },
          "tags": [
            "文档"
          ]
        }
      },
      "/api/v1/document/list": {
        "post": {
          "operationId": "DocumentController_list",
          "summary": "系统知识库文档分页查询 •【Public】🔑",
          "parameters": [],
          "requestBody": {
            "required": true,
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/ListDocBodyDto"
                }
              }
            }
          },
          "responses": {
            "200": {
              "description": "",
              "content": {
                "application/json": {
                  "schema": {
                    "allOf": [
                      {
                        "$ref": "#/components/schemas/ResponseDto"
                      },
                      {
                        "properties": {
                          "data": {
                            "allOf": [
                              {
                                "$ref": "#/components/schemas/PaginatedDto"
                              },
                              {
                                "properties": {
                                  "list": {
                                    "type": "array",
                                    "items": {
                                      "$ref": "#/components/schemas/DocumentDtoDetailDto"
                                    }
                                  }
                                }
                              }
                            ]
                          }
                        }
                      }
                    ]
                  }
                }
              }
            }
          },
          "tags": [
            "文档"
          ]
        }
      },
      "/api/v1/document/list/by/filter": {
        "post": {
          "operationId": "DocumentController_listByIds",
          "summary": "用户通过ids/filename查询文档",
          "parameters": [],
          "requestBody": {
            "required": true,
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/ListByFilterDto"
                }
              }
            }
          },
          "responses": {
            "200": {
              "description": "",
              "content": {
                "application/json": {
                  "schema": {
                    "allOf": [
                      {
                        "$ref": "#/components/schemas/ResponseDto"
                      },
                      {
                        "properties": {
                          "data": {
                            "type": "array",
                            "items": {
                              "$ref": "#/components/schemas/DocumentDtoDetailDto"
                            }
                          }
                        }
                      }
                    ]
                  }
                }
              }
            }
          },
          "tags": [
            "文档"
          ]
        }
      },
      "/api/v1/document/list/by": {
        "post": {
          "operationId": "DocumentController_listByUuids",
          "summary": "用户通过uuids查询文档",
          "parameters": [],
          "requestBody": {
            "required": true,
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/ListByFilterDto"
                }
              }
            }
          },
          "responses": {
            "200": {
              "description": "",
              "content": {
                "application/json": {
                  "schema": {
                    "allOf": [
                      {
                        "$ref": "#/components/schemas/ResponseDto"
                      },
                      {
                        "properties": {
                          "data": {
                            "type": "array",
                            "items": {
                              "$ref": "#/components/schemas/DocumentDtoDetailDto"
                            }
                          }
                        }
                      }
                    ]
                  }
                }
              }
            }
          },
          "tags": [
            "文档"
          ]
        }
      },
      "/api/v1/document/info": {
        "get": {
          "operationId": "DocumentController_getInfo",
          "summary": "id查询",
          "parameters": [],
          "responses": {
            "200": {
              "description": ""
            }
          },
          "tags": [
            "文档"
          ]
        }
      },
      "/api/v1/document/list/public": {
        "post": {
          "operationId": "DocumentController_InternalListByIds",
          "summary": "查询企业知识库 •【Public】🔑",
          "parameters": [],
          "requestBody": {
            "required": true,
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/ListByFilterDto"
                }
              }
            }
          },
          "responses": {
            "200": {
              "description": "",
              "content": {
                "application/json": {
                  "schema": {
                    "allOf": [
                      {
                        "$ref": "#/components/schemas/ResponseDto"
                      },
                      {
                        "properties": {
                          "data": {
                            "type": "array",
                            "items": {
                              "$ref": "#/components/schemas/DocumentDtoDetailDto"
                            }
                          }
                        }
                      }
                    ]
                  }
                }
              }
            }
          },
          "tags": [
            "文档"
          ]
        }
      },
      "/api/v1/document/list/personal": {
        "post": {
          "operationId": "DocumentController_listByUser",
          "summary": "查询个人知识库",
          "parameters": [],
          "requestBody": {
            "required": true,
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/ListByUserDto"
                }
              }
            }
          },
          "responses": {
            "200": {
              "description": "",
              "content": {
                "application/json": {
                  "schema": {
                    "allOf": [
                      {
                        "$ref": "#/components/schemas/ResponseDto"
                      },
                      {
                        "properties": {
                          "data": {
                            "type": "array",
                            "items": {
                              "$ref": "#/components/schemas/DocumentDtoDetailDto"
                            }
                          }
                        }
                      }
                    ]
                  }
                }
              }
            }
          },
          "tags": [
            "文档"
          ]
        }
      },
      "/api/v1/document/delete": {
        "post": {
          "operationId": "DocumentController_delete",
          "summary": "文档删除",
          "parameters": [],
          "requestBody": {
            "required": true,
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/DocIdListDto"
                }
              }
            }
          },
          "responses": {
            "200": {
              "description": "",
              "content": {
                "application/json": {
                  "schema": {
                    "allOf": [
                      {
                        "$ref": "#/components/schemas/ResponseDto"
                      },
                      {
                        "properties": {
                          "data": {
                            "type": "boolean"
                          }
                        }
                      }
                    ]
                  }
                }
              }
            }
          },
          "tags": [
            "文档"
          ]
        }
      },
      "/api/v1/document/admin/delete": {
        "post": {
          "operationId": "DocumentController_deleteByAdmin",
          "parameters": [],
          "responses": {
            "201": {
              "description": ""
            }
          },
          "tags": [
            "文档"
          ]
        }
      },
      "/api/v1/document/move": {
        "post": {
          "operationId": "DocumentController_move",
          "summary": "修改文档所属文件夹",
          "parameters": [],
          "requestBody": {
            "required": true,
            "content": {
              "application/json": {
                "schema": {
                  "type": "array",
                  "items": {
                    "$ref": "#/components/schemas/DocumentFolderMoveDto"
                  }
                }
              }
            }
          },
          "responses": {
            "200": {
              "description": "",
              "content": {
                "application/json": {
                  "schema": {
                    "allOf": [
                      {
                        "$ref": "#/components/schemas/ResponseDto"
                      },
                      {
                        "properties": {
                          "data": {
                            "type": "boolean"
                          }
                        }
                      }
                    ]
                  }
                }
              }
            }
          },
          "tags": [
            "文档"
          ]
        }
      },
      "/api/v1/document/update": {
        "post": {
          "operationId": "DocumentController_update",
          "summary": "修改文档信息",
          "parameters": [],
          "requestBody": {
            "required": true,
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/UpdateDocDto"
                }
              }
            }
          },
          "responses": {
            "200": {
              "description": "",
              "content": {
                "application/json": {
                  "schema": {
                    "allOf": [
                      {
                        "$ref": "#/components/schemas/ResponseDto"
                      },
                      {
                        "properties": {
                          "data": {
                            "$ref": "#/components/schemas/DocumentDto"
                          }
                        }
                      }
                    ]
                  }
                }
              }
            }
          },
          "tags": [
            "文档"
          ]
        }
      },
      "/api/v1/document/folder/sort": {
        "post": {
          "operationId": "DocumentController_sort",
          "summary": "修改文档/文件夹顺序",
          "parameters": [],
          "requestBody": {
            "required": true,
            "content": {
              "application/json": {
                "schema": {
                  "type": "array",
                  "items": {
                    "$ref": "#/components/schemas/DocumentSortDto"
                  }
                }
              }
            }
          },
          "responses": {
            "200": {
              "description": "",
              "content": {
                "application/json": {
                  "schema": {
                    "allOf": [
                      {
                        "$ref": "#/components/schemas/ResponseDto"
                      },
                      {
                        "properties": {
                          "data": {
                            "type": "boolean"
                          }
                        }
                      }
                    ]
                  }
                }
              }
            }
          },
          "tags": [
            "文档"
          ]
        }
      },
      "/api/v1/document/reparse": {
        "get": {
          "operationId": "DocumentController_reparse",
          "summary": "文档重新解析",
          "parameters": [
            {
              "name": "id",
              "required": true,
              "in": "query",
              "description": "文档id",
              "schema": {
                "type": "number"
              }
            }
          ],
          "responses": {
            "200": {
              "description": "",
              "content": {
                "application/json": {
                  "schema": {
                    "allOf": [
                      {
                        "$ref": "#/components/schemas/ResponseDto"
                      },
                      {
                        "properties": {
                          "data": {
                            "type": "boolean"
                          }
                        }
                      }
                    ]
                  }
                }
              }
            }
          },
          "tags": [
            "文档"
          ]
        }
      },
      "/api/v1/document/download": {
        "get": {
          "operationId": "DocumentController_download",
          "summary": "文档下载",
          "parameters": [
            {
              "name": "id",
              "required": true,
              "in": "query",
              "description": "文档id",
              "schema": {
                "type": "string"
              }
            },
            {
              "name": "type",
              "required": true,
              "in": "query",
              "description": "类型",
              "schema": {
                "enum": [
                  "source",
                  "imageList",
                  "docparser",
                  "catalog",
                  "merge",
                  "brief"
                ],
                "type": "string"
              }
            },
            {
              "name": "image_id",
              "required": true,
              "in": "query",
              "description": "图片id",
              "schema": {
                "type": "string"
              }
            },
            {
              "name": "document_type",
              "required": false,
              "in": "query",
              "description": "文档类型",
              "schema": {
                "enum": [
                  0,
                  1
                ],
                "type": "number"
              }
            }
          ],
          "responses": {
            "200": {
              "description": ""
            }
          },
          "tags": [
            "文档"
          ]
        }
      },
      "/api/v1/document/callback": {
        "get": {
          "operationId": "DocumentController_getCallback",
          "summary": "文档状态回调 •【Internal】🔒",
          "parameters": [
            {
              "name": "uuid",
              "required": true,
              "in": "query",
              "description": "文档uuid",
              "schema": {
                "type": "string"
              }
            },
            {
              "name": "status",
              "required": true,
              "in": "query",
              "description": "状态(上传完成,docparser解析成功,目录解析成功,成功,失败)",
              "schema": {
                "enum": [
                  1,
                  2,
                  3,
                  4,
                  5,
                  -1
                ],
                "type": "number"
              }
            },
            {
              "name": "message",
              "required": false,
              "in": "query",
              "description": "信息",
              "schema": {
                "type": "string"
              }
            },
            {
              "description": "文档总页数",
              "required": false,
              "name": "page_number",
              "in": "query",
              "schema": {
                "type": "number"
              }
            },
            {
              "description": "第一页图片ID",
              "required": false,
              "name": "first_image_id",
              "in": "query",
              "schema": {
                "type": "string"
              }
            },
            {
              "description": "系统知识库：0，个人知识库：User_1（User_{user_id}）",
              "required": false,
              "name": "knowledge_id",
              "in": "query",
              "schema": {
                "type": "string"
              }
            },
            {
              "description": "文档所属（系统知识库、个人知识库）",
              "required": false,
              "name": "ori_type",
              "in": "query",
              "schema": {
                "type": "string"
              }
            }
          ],
          "responses": {
            "200": {
              "description": ""
            }
          },
          "tags": [
            "文档"
          ]
        },
        "post": {
          "operationId": "DocumentController_postCallback",
          "summary": "文档状态回调 •【Internal】🔒",
          "parameters": [],
          "requestBody": {
            "required": true,
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/CallbackDto"
                }
              }
            }
          },
          "responses": {
            "201": {
              "description": ""
            }
          },
          "tags": [
            "文档"
          ]
        }
      },
      "/api/v1/document/summary": {
        "post": {
          "operationId": "DocumentController_summary",
          "summary": "文档概要更新/查询 •【Public】🔑",
          "description": "查询: id; 保存: uuid + data; 重新生成: id + regeneration",
          "parameters": [],
          "requestBody": {
            "required": true,
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/DocSummaryDto"
                }
              }
            }
          },
          "responses": {
            "201": {
              "description": ""
            }
          },
          "tags": [
            "文档"
          ]
        }
      },
      "/api/v1/document/filter/config": {
        "get": {
          "operationId": "DocumentController_filterConfigList",
          "summary": "文档的查询配置 •【Public】🔑",
          "parameters": [],
          "responses": {
            "200": {
              "description": "",
              "content": {
                "application/json": {
                  "schema": {
                    "allOf": [
                      {
                        "$ref": "#/components/schemas/ResponseDto"
                      },
                      {
                        "properties": {
                          "data": {
                            "$ref": "#/components/schemas/FilterConfigDto"
                          }
                        }
                      }
                    ]
                  }
                }
              }
            }
          },
          "tags": [
            "文档"
          ]
        }
      },
      "/api/v1/chat/infer": {
        "post": {
          "operationId": "ChatController_create",
          "summary": "提问",
          "parameters": [],
          "requestBody": {
            "required": true,
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/CreateChatDto"
                }
              }
            }
          },
          "responses": {
            "200": {
              "description": "",
              "content": {
                "application/json": {
                  "schema": {
                    "allOf": [
                      {
                        "$ref": "#/components/schemas/ResponseDto"
                      },
                      {
                        "properties": {
                          "data": {
                            "$ref": "#/components/schemas/ChatContentResDto"
                          }
                        }
                      }
                    ]
                  }
                }
              }
            }
          },
          "tags": [
            "对话"
          ]
        }
      },
      "/api/v1/chat/global/infer": {
        "post": {
          "operationId": "ChatController_globalChat",
          "summary": "全局提问",
          "parameters": [],
          "requestBody": {
            "required": true,
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/CreateGlobalChatDto"
                }
              }
            }
          },
          "responses": {
            "200": {
              "description": "",
              "content": {
                "application/json": {
                  "schema": {
                    "allOf": [
                      {
                        "$ref": "#/components/schemas/ResponseDto"
                      },
                      {
                        "properties": {
                          "data": {
                            "$ref": "#/components/schemas/ChatContentResDto"
                          }
                        }
                      }
                    ]
                  }
                }
              }
            }
          },
          "tags": [
            "对话"
          ]
        }
      },
      "/api/v1/chat/recommend": {
        "post": {
          "operationId": "ChatController_recommend",
          "summary": "推荐问题",
          "parameters": [],
          "requestBody": {
            "required": true,
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/RecommendDto"
                }
              }
            }
          },
          "responses": {
            "200": {
              "description": "",
              "content": {
                "application/json": {
                  "schema": {
                    "allOf": [
                      {
                        "$ref": "#/components/schemas/ResponseDto"
                      },
                      {
                        "properties": {
                          "data": {
                            "type": "array",
                            "items": {
                              "type": "string"
                            }
                          }
                        }
                      }
                    ]
                  }
                }
              }
            }
          },
          "tags": [
            "对话"
          ]
        }
      },
      "/api/v1/chat/history": {
        "get": {
          "operationId": "ChatController_history",
          "summary": "历史问题列表",
          "parameters": [
            {
              "name": "documentId",
              "required": false,
              "in": "query",
              "description": "文档id",
              "schema": {
                "type": "array",
                "items": {
                  "type": "string"
                }
              }
            },
            {
              "name": "num",
              "required": false,
              "in": "query",
              "description": "数量",
              "schema": {
                "type": "number"
              }
            }
          ],
          "responses": {
            "200": {
              "description": "",
              "content": {
                "application/json": {
                  "schema": {
                    "allOf": [
                      {
                        "$ref": "#/components/schemas/ResponseDto"
                      },
                      {
                        "properties": {
                          "data": {
                            "type": "array",
                            "items": {
                              "$ref": "#/components/schemas/ChatResDto"
                            }
                          }
                        }
                      }
                    ]
                  }
                }
              }
            }
          },
          "tags": [
            "对话"
          ]
        }
      },
      "/api/v1/chat/history/detail": {
        "get": {
          "operationId": "ChatController_historyDetail",
          "summary": "历史问题对话明细",
          "parameters": [
            {
              "name": "chatId",
              "required": true,
              "in": "query",
              "description": "对话id",
              "schema": {
                "type": "number"
              }
            },
            {
              "name": "endContentId",
              "required": false,
              "in": "query",
              "description": "加载该contentId之前的数据",
              "schema": {
                "type": "number"
              }
            },
            {
              "name": "num",
              "required": false,
              "in": "query",
              "description": "加载数量",
              "schema": {
                "default": 50,
                "type": "number"
              }
            }
          ],
          "responses": {
            "200": {
              "description": "",
              "content": {
                "application/json": {
                  "schema": {
                    "allOf": [
                      {
                        "$ref": "#/components/schemas/ResponseDto"
                      },
                      {
                        "properties": {
                          "data": {
                            "allOf": [
                              {
                                "$ref": "#/components/schemas/PaginatedDto"
                              },
                              {
                                "properties": {
                                  "list": {
                                    "type": "array",
                                    "items": {
                                      "$ref": "#/components/schemas/ChatContentResDto"
                                    }
                                  }
                                }
                              }
                            ]
                          }
                        }
                      }
                    ]
                  }
                }
              }
            }
          },
          "tags": [
            "对话"
          ]
        }
      },
      "/api/v1/chat/answer/detail": {
        "post": {
          "operationId": "ChatController_contentDetail",
          "summary": "回答明细",
          "parameters": [],
          "requestBody": {
            "required": true,
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/AnswerIdsDto"
                }
              }
            }
          },
          "responses": {
            "200": {
              "description": "",
              "content": {
                "application/json": {
                  "schema": {
                    "allOf": [
                      {
                        "$ref": "#/components/schemas/ResponseDto"
                      },
                      {
                        "properties": {
                          "data": {
                            "type": "array",
                            "items": {
                              "$ref": "#/components/schemas/ChatContentResDto"
                            }
                          }
                        }
                      }
                    ]
                  }
                }
              }
            }
          },
          "tags": [
            "对话"
          ]
        }
      },
      "/api/v1/chat/feedback": {
        "post": {
          "operationId": "ChatController_feedback",
          "summary": "反馈",
          "parameters": [],
          "requestBody": {
            "required": true,
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/FeedbackDto"
                }
              }
            }
          },
          "responses": {
            "200": {
              "description": "",
              "content": {
                "application/json": {
                  "schema": {
                    "allOf": [
                      {
                        "$ref": "#/components/schemas/ResponseDto"
                      },
                      {
                        "properties": {
                          "data": {
                            "$ref": "#/components/schemas/ChatContentResDto"
                          }
                        }
                      }
                    ]
                  }
                }
              }
            }
          },
          "tags": [
            "对话"
          ]
        }
      },
      "/api/v1/chat/history/update": {
        "post": {
          "operationId": "ChatController_updateHistory",
          "summary": "更新历史对话标题",
          "parameters": [],
          "requestBody": {
            "required": true,
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/UpdateChatDto"
                }
              }
            }
          },
          "responses": {
            "200": {
              "description": "",
              "content": {
                "application/json": {
                  "schema": {
                    "allOf": [
                      {
                        "$ref": "#/components/schemas/ResponseDto"
                      },
                      {
                        "properties": {
                          "data": {
                            "$ref": "#/components/schemas/ChatResDto"
                          }
                        }
                      }
                    ]
                  }
                }
              }
            }
          },
          "tags": [
            "对话"
          ]
        }
      },
      "/api/v1/chat/history/delete": {
        "post": {
          "operationId": "ChatController_deleteHistory",
          "summary": "删除历史对话",
          "parameters": [],
          "requestBody": {
            "required": true,
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/IdsChatDto"
                }
              }
            }
          },
          "responses": {
            "200": {
              "description": "",
              "content": {
                "application/json": {
                  "schema": {
                    "allOf": [
                      {
                        "$ref": "#/components/schemas/ResponseDto"
                      },
                      {
                        "properties": {
                          "data": {
                            "type": "boolean"
                          }
                        }
                      }
                    ]
                  }
                }
              }
            }
          },
          "tags": [
            "对话"
          ]
        }
      },
      "/api/v1/chat/qa/list": {
        "post": {
          "operationId": "ChatController_qaList",
          "summary": "个人中心问答记录分页查询",
          "parameters": [],
          "requestBody": {
            "required": true,
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/ListChatBodyDto"
                }
              }
            }
          },
          "responses": {
            "200": {
              "description": "",
              "content": {
                "application/json": {
                  "schema": {
                    "allOf": [
                      {
                        "$ref": "#/components/schemas/ResponseDto"
                      },
                      {
                        "properties": {
                          "data": {
                            "allOf": [
                              {
                                "$ref": "#/components/schemas/PaginatedDto"
                              },
                              {
                                "properties": {
                                  "list": {
                                    "type": "array",
                                    "items": {
                                      "$ref": "#/components/schemas/ChatContentListResDto"
                                    }
                                  }
                                }
                              }
                            ]
                          }
                        }
                      }
                    ]
                  }
                }
              }
            }
          },
          "tags": [
            "对话"
          ]
        }
      },
      "/api/v1/chat/statistics": {
        "post": {
          "operationId": "ChatController_statistics",
          "summary": "概览问答次数统计",
          "parameters": [],
          "requestBody": {
            "required": true,
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/StatisticsDto"
                }
              }
            }
          },
          "responses": {
            "200": {
              "description": "",
              "content": {
                "application/json": {
                  "schema": {
                    "allOf": [
                      {
                        "$ref": "#/components/schemas/ResponseDto"
                      },
                      {
                        "properties": {
                          "data": {
                            "$ref": "#/components/schemas/StatisticsResDto"
                          }
                        }
                      }
                    ]
                  }
                }
              }
            }
          },
          "tags": [
            "对话"
          ]
        }
      },
      "/api/v1/recycle/list": {
        "post": {
          "operationId": "RecycleController_recycleList",
          "summary": "回收站列表分页查询",
          "parameters": [],
          "requestBody": {
            "required": true,
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/RecycleListQueryDto"
                }
              }
            }
          },
          "responses": {
            "200": {
              "description": "",
              "content": {
                "application/json": {
                  "schema": {
                    "allOf": [
                      {
                        "$ref": "#/components/schemas/ResponseDto"
                      },
                      {
                        "properties": {
                          "data": {
                            "allOf": [
                              {
                                "$ref": "#/components/schemas/PaginatedDto"
                              },
                              {
                                "properties": {
                                  "list": {
                                    "type": "array",
                                    "items": {
                                      "$ref": "#/components/schemas/RecycleItemDto"
                                    }
                                  }
                                }
                              }
                            ]
                          }
                        }
                      }
                    ]
                  }
                }
              }
            }
          },
          "tags": [
            "回收站"
          ]
        }
      },
      "/api/v1/recycle/restore": {
        "post": {
          "operationId": "RecycleController_recycleRestore",
          "summary": "回收站恢复",
          "parameters": [],
          "requestBody": {
            "required": true,
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/RecycleIdListDto"
                }
              }
            }
          },
          "responses": {
            "200": {
              "description": "",
              "content": {
                "application/json": {
                  "schema": {
                    "allOf": [
                      {
                        "$ref": "#/components/schemas/ResponseDto"
                      },
                      {
                        "properties": {
                          "data": {
                            "type": "boolean"
                          }
                        }
                      }
                    ]
                  }
                }
              }
            }
          },
          "tags": [
            "回收站"
          ]
        }
      },
      "/api/v1/recycle/delete": {
        "post": {
          "operationId": "RecycleController_recycleDelete",
          "summary": "回收站删除",
          "parameters": [],
          "requestBody": {
            "required": true,
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/RecycleIdListDto"
                }
              }
            }
          },
          "responses": {
            "200": {
              "description": "",
              "content": {
                "application/json": {
                  "schema": {
                    "allOf": [
                      {
                        "$ref": "#/components/schemas/ResponseDto"
                      },
                      {
                        "properties": {
                          "data": {
                            "type": "boolean"
                          }
                        }
                      }
                    ]
                  }
                }
              }
            }
          },
          "tags": [
            "回收站"
          ]
        }
      },
      "/api/v1/common/config/detail": {
        "get": {
          "operationId": "ManagerController_detail",
          "summary": "配置查询 •【Public】🔑",
          "description": "concept概念/industry行业/financeType类型...",
          "parameters": [
            {
              "name": "key",
              "required": true,
              "in": "query",
              "schema": {
                "type": "string"
              }
            }
          ],
          "responses": {
            "200": {
              "description": "",
              "content": {
                "application/json": {
                  "schema": {
                    "allOf": [
                      {
                        "$ref": "#/components/schemas/ResponseDto"
                      },
                      {
                        "properties": {
                          "data": {
                            "$ref": "#/components/schemas/UpdateConfigDto"
                          }
                        }
                      }
                    ]
                  }
                }
              }
            }
          },
          "tags": [
            "公共接口"
          ]
        }
      },
      "/api/v1/common/config/update": {
        "post": {
          "operationId": "ManagerController_update",
          "summary": "配置修改 •【Admin】🔐",
          "parameters": [],
          "requestBody": {
            "required": true,
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/UpdateConfigDto"
                }
              }
            }
          },
          "responses": {
            "200": {
              "description": "",
              "content": {
                "application/json": {
                  "schema": {
                    "allOf": [
                      {
                        "$ref": "#/components/schemas/ResponseDto"
                      },
                      {
                        "properties": {
                          "data": {
                            "$ref": "#/components/schemas/UpdateConfigDto"
                          }
                        }
                      }
                    ]
                  }
                }
              }
            }
          },
          "tags": [
            "公共接口"
          ]
        }
      },
      "/api/v1/common/public/upload": {
        "post": {
          "operationId": "ManagerController_publicUpload",
          "summary": "上传静态资源 •【Admin】🔐",
          "parameters": [
            {
              "name": "type",
              "required": false,
              "in": "query",
              "description": "type",
              "schema": {
                "enum": [
                  "avatar",
                  "cover"
                ],
                "type": "string"
              }
            },
            {
              "name": "uuid",
              "required": false,
              "in": "query",
              "description": "uuid",
              "schema": {
                "type": "string"
              }
            }
          ],
          "requestBody": {
            "required": true,
            "content": {
              "application/octet-stream": {
                "schema": {
                  "format": "binary"
                }
              }
            }
          },
          "responses": {
            "201": {
              "description": ""
            }
          },
          "tags": [
            "公共接口"
          ]
        }
      },
      "/api/v1/common/public/download": {
        "get": {
          "operationId": "ManagerController_publicDownload",
          "summary": "静态资源下载 •【Public】🔑",
          "description": "封面：cover + 文档uuid;\n 头像：avatar + 用户id;\n 为空：公开的静态资源",
          "parameters": [
            {
              "name": "type",
              "required": false,
              "in": "query",
              "description": "type",
              "schema": {
                "enum": [
                  "avatar",
                  "cover"
                ],
                "type": "string"
              }
            },
            {
              "name": "path",
              "required": true,
              "in": "query",
              "description": "uuid",
              "schema": {
                "type": "string"
              }
            }
          ],
          "responses": {
            "200": {
              "description": ""
            }
          },
          "tags": [
            "公共接口"
          ]
        }
      },
      "/api/v1/common/sms": {
        "post": {
          "operationId": "ManagerController_sendSMS",
          "summary": "发送短信验证码 •【Public】🔑",
          "parameters": [],
          "requestBody": {
            "required": true,
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/ISmsDto"
                }
              }
            }
          },
          "responses": {
            "201": {
              "description": ""
            }
          },
          "tags": [
            "公共接口"
          ]
        }
      },
      "/api/v1/common/global/search": {
        "post": {
          "operationId": "ManagerController_globalSearch",
          "summary": "全局搜索",
          "parameters": [],
          "requestBody": {
            "required": true,
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/GlobalSearchDto"
                }
              }
            }
          },
          "responses": {
            "201": {
              "description": ""
            }
          },
          "tags": [
            "公共接口"
          ]
        }
      },
      "/api/v1/common/pdf-to-word": {
        "post": {
          "operationId": "ManagerController_pdfToWord",
          "summary": "pdf to word",
          "parameters": [],
          "requestBody": {
            "required": true,
            "content": {
              "application/octet-stream": {
                "schema": {
                  "format": "binary"
                }
              }
            }
          },
          "responses": {
            "201": {
              "description": ""
            }
          },
          "tags": [
            "公共接口"
          ]
        }
      },
      "/api/v1/common/pdf-to-word/v2": {
        "post": {
          "operationId": "ManagerController_pdfToWordV2",
          "summary": "pdf to word v2",
          "parameters": [],
          "requestBody": {
            "required": true,
            "content": {
              "application/octet-stream": {
                "schema": {
                  "format": "binary"
                }
              }
            }
          },
          "responses": {
            "201": {
              "description": ""
            }
          },
          "tags": [
            "公共接口"
          ]
        }
      },
      "/api/v1/common/document/all": {
        "post": {
          "operationId": "ManagerController_listAll",
          "summary": "获取所有文档 •【Internal】🔒",
          "parameters": [],
          "requestBody": {
            "required": true,
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/DocAllQueryDto"
                }
              }
            }
          },
          "responses": {
            "201": {
              "description": ""
            }
          },
          "tags": [
            "公共接口"
          ]
        }
      },
      "/api/v1/common/delete/all": {
        "post": {
          "operationId": "ManagerController_deleteAll",
          "parameters": [],
          "responses": {
            "201": {
              "description": ""
            }
          },
          "tags": [
            "公共接口"
          ]
        }
      },
      "/api/v1/hotspots": {
        "get": {
          "operationId": "HotspotsController_getHotspot",
          "summary": "查询热门内容 •【Public】🔑",
          "parameters": [],
          "responses": {
            "200": {
              "description": "",
              "content": {
                "application/json": {
                  "schema": {
                    "allOf": [
                      {
                        "$ref": "#/components/schemas/ResponseDto"
                      },
                      {
                        "properties": {
                          "data": {
                            "$ref": "#/components/schemas/HotspotsDetailDto"
                          }
                        }
                      }
                    ]
                  }
                }
              }
            }
          },
          "tags": [
            "热门"
          ]
        }
      }
    },
    "info": {
      "title": "gpt-qa API文档",
      "description": "",
      "version": "1.0",
      "contact": {}
    },
    "tags": [],
    "servers": [],
    "components": {
      "schemas": {
        "UserDetailDto": {
          "type": "object",
          "properties": {
            "id": {
              "type": "number"
            },
            "account": {
              "type": "string"
            },
            "role": {
              "type": "number",
              "description": "用户角色(超级管理员/普通管理员/普通用户)",
              "enum": [
                0,
                1,
                2
              ]
            },
            "mobile": {
              "type": "string"
            },
            "email": {
              "type": "string"
            },
            "avatar": {
              "type": "string"
            },
            "createTime": {
              "format": "date-time",
              "type": "string"
            },
            "updateTime": {
              "format": "date-time",
              "type": "string"
            }
          },
          "required": [
            "id",
            "account",
            "role",
            "mobile",
            "email",
            "avatar",
            "createTime",
            "updateTime"
          ]
        },
        "UserLoginDto": {
          "type": "object",
          "properties": {
            "openid": {
              "type": "string",
              "description": "textin openid"
            },
            "name": {
              "type": "string",
              "description": "名称"
            },
            "account": {
              "type": "string",
              "description": "账号"
            },
            "password": {
              "type": "string",
              "description": "密码(MD5加密)"
            },
            "mobile": {
              "type": "string",
              "description": "手机号",
              "example": null
            },
            "mobileAreaCode": {
              "type": "string",
              "description": "手机号国际区号",
              "example": "86"
            },
            "email": {
              "type": "string",
              "description": "邮箱",
              "example": null
            },
            "code": {
              "type": "string",
              "description": "验证码",
              "example": null
            }
          }
        },
        "ResponseDto": {
          "type": "object",
          "properties": {
            "code": {
              "type": "number",
              "enum": [
                100,
                101,
                102,
                103,
                200,
                201,
                202,
                203,
                204,
                205,
                206,
                207,
                208,
                226,
                300,
                301,
                302,
                303,
                304,
                305,
                306,
                307,
                308,
                400,
                401,
                402,
                403,
                404,
                405,
                406,
                407,
                408,
                409,
                410,
                411,
                412,
                413,
                414,
                415,
                416,
                417,
                418,
                421,
                422,
                423,
                424,
                425,
                426,
                428,
                429,
                431,
                451,
                500,
                501,
                502,
                503,
                504,
                505,
                506,
                507,
                508,
                510,
                511
              ],
              "example": 200
            },
            "msg": {
              "type": "string",
              "example": "success"
            }
          },
          "required": [
            "code",
            "msg"
          ]
        },
        "UserRegisterDto": {
          "type": "object",
          "properties": {
            "account": {
              "type": "string",
              "description": "账号",
              "example": null
            },
            "mobile": {
              "type": "string",
              "description": "手机号",
              "example": null
            },
            "mobileAreaCode": {
              "type": "string",
              "description": "手机号国际区号",
              "example": "86"
            },
            "email": {
              "type": "string",
              "description": "邮箱",
              "example": null
            },
            "password": {
              "type": "string",
              "description": "密码(MD5加密)"
            }
          },
          "required": [
            "password"
          ]
        },
        "UserUpdatePassword": {
          "type": "object",
          "properties": {
            "account": {
              "type": "string",
              "description": "账号",
              "default": null
            },
            "newPassword": {
              "type": "string",
              "description": "新密码(MD5加密)"
            }
          },
          "required": [
            "newPassword"
          ]
        },
        "UpdateUserKeyInfoDto": {
          "type": "object",
          "properties": {
            "id": {
              "type": "number",
              "description": "用户id"
            },
            "account": {
              "type": "string",
              "description": "账号"
            },
            "email": {
              "type": "string",
              "description": "邮箱"
            },
            "mobile": {
              "type": "string",
              "description": "手机号"
            },
            "role": {
              "type": "number",
              "description": "用户角色(超级管理员/普通管理员/普通用户)",
              "enum": [
                0,
                1,
                2
              ],
              "default": 2
            },
            "status": {
              "type": "number",
              "description": "用户状态",
              "enum": [
                1,
                10,
                20
              ],
              "default": 1
            }
          },
          "required": [
            "id"
          ]
        },
        "UpdateUserInfoDto": {
          "type": "object",
          "properties": {
            "name": {
              "type": "string",
              "description": "名称"
            },
            "avatar": {
              "type": "string",
              "description": "头像"
            }
          }
        },
        "SearchUserInfoDto": {
          "type": "object",
          "properties": {
            "id": {
              "type": "number",
              "description": "用户id"
            },
            "account": {
              "type": "string",
              "description": "账号"
            },
            "email": {
              "type": "string",
              "description": "邮箱"
            },
            "mobile": {
              "type": "string",
              "description": "手机号"
            },
            "role": {
              "description": "用户角色(超级管理员/普通管理员/普通用户)",
              "type": "array",
              "items": {
                "type": "number"
              }
            },
            "status": {
              "type": "number",
              "description": "用户状态(正常/禁用账号/禁用提问)",
              "enum": [
                1,
                10,
                20
              ]
            },
            "createTime": {
              "description": "创建时间",
              "example": [
                "2025-03-25T10:32:16.534Z",
                "2025-03-25T10:32:16.534Z"
              ],
              "type": "array",
              "items": {
                "format": "date-time",
                "type": "string"
              }
            }
          },
          "required": [
            "createTime"
          ]
        },
        "LibraryDetailDto": {
          "type": "object",
          "properties": {
            "id": {
              "type": "number"
            },
            "name": {
              "type": "string"
            },
            "note": {
              "type": "string"
            },
            "type": {
              "type": "number",
              "enum": [
                0,
                10
              ]
            },
            "createTime": {
              "format": "date-time",
              "type": "string"
            },
            "updateTime": {
              "format": "date-time",
              "type": "string"
            }
          },
          "required": [
            "id",
            "name",
            "note",
            "type",
            "createTime",
            "updateTime"
          ]
        },
        "CreateLibraryDto": {
          "type": "object",
          "properties": {
            "name": {
              "type": "string",
              "description": "知识库名称"
            },
            "note": {
              "type": "string",
              "description": "知识库描述"
            },
            "summary": {
              "type": "string",
              "description": "知识库描述摘要"
            },
            "type": {
              "type": "number",
              "description": "知识库类型(自定义知识库:10)",
              "enum": [
                0,
                10
              ]
            }
          },
          "required": [
            "name",
            "note",
            "summary",
            "type"
          ]
        },
        "UpdateLibraryDto": {
          "type": "object",
          "properties": {
            "id": {
              "type": "number",
              "description": "知识库id"
            },
            "name": {
              "type": "string",
              "description": "知识库名称"
            },
            "note": {
              "type": "string",
              "description": "知识库描述"
            },
            "summary": {
              "type": "string",
              "description": "知识库描述摘要"
            }
          },
          "required": [
            "id",
            "name",
            "note"
          ]
        },
        "LibraryDeleteDto": {
          "type": "object",
          "properties": {
            "ids": {
              "description": "知识库id集合",
              "type": "array",
              "items": {
                "type": "number"
              }
            }
          },
          "required": [
            "ids"
          ]
        },
        "LibraryTreeDto": {
          "type": "object",
          "properties": {
            "noDocument": {
              "type": "boolean",
              "description": "不返回文档",
              "default": false
            }
          }
        },
        "FolderDetailDto": {
          "type": "object",
          "properties": {
            "id": {
              "type": "number"
            },
            "name": {
              "type": "string"
            },
            "userId": {
              "type": "number"
            },
            "libraryId": {
              "type": "number"
            },
            "createTime": {
              "format": "date-time",
              "type": "string"
            },
            "updateTime": {
              "format": "date-time",
              "type": "string"
            }
          },
          "required": [
            "id",
            "name",
            "userId",
            "libraryId",
            "createTime",
            "updateTime"
          ]
        },
        "CreateFolderDto": {
          "type": "object",
          "properties": {
            "name": {
              "type": "string",
              "description": "文件夹名称"
            },
            "parentId": {
              "type": "number",
              "description": "父级文件夹id"
            }
          },
          "required": [
            "name"
          ]
        },
        "UpdateFolderDto": {
          "type": "object",
          "properties": {
            "id": {
              "type": "number",
              "description": "文件夹id"
            },
            "name": {
              "type": "string",
              "description": "文件夹名称"
            }
          },
          "required": [
            "id",
            "name"
          ]
        },
        "FolderDeleteDto": {
          "type": "object",
          "properties": {
            "ids": {
              "description": "文件夹id集合",
              "type": "array",
              "items": {
                "type": "number"
              }
            },
            "deleteDocument": {
              "type": "boolean",
              "description": "是否同时删除文档",
              "default": true
            }
          },
          "required": [
            "ids",
            "deleteDocument"
          ]
        },
        "MoveFolderDto": {
          "type": "object",
          "properties": {
            "id": {
              "type": "number",
              "description": "文件夹id"
            },
            "targetId": {
              "type": "number",
              "description": "目标位置id(文件夹id或者null)"
            }
          },
          "required": [
            "id"
          ]
        },
        "ChildrenQueryDto": {
          "type": "object",
          "properties": {
            "id": {
              "type": "number",
              "description": "id"
            },
            "noChildTree": {
              "type": "boolean",
              "description": "不显示children树状数据"
            },
            "keyword": {
              "type": "string",
              "description": "搜索"
            },
            "sort": {
              "type": "string",
              "description": "排序",
              "enum": [
                "recentUpdate",
                "recentUsed",
                "createTime",
                "updateTime",
                "size",
                "name"
              ]
            },
            "sortType": {
              "type": "string",
              "description": "升序/降序",
              "enum": [
                "ASC",
                "DESC"
              ]
            }
          }
        },
        "DocumentExtraDataDto": {
          "type": "object",
          "properties": {
            "company": {
              "type": "string",
              "description": "企业名称"
            },
            "stockSymbol": {
              "type": "string",
              "description": "股票代码"
            },
            "financeDate": {
              "format": "date-time",
              "type": "string",
              "description": "财报时间"
            },
            "financeType": {
              "type": "string",
              "description": "财报类型"
            },
            "industry": {
              "description": "行业",
              "type": "array",
              "items": {
                "type": "string"
              }
            },
            "concept": {
              "description": "概念",
              "type": "array",
              "items": {
                "type": "string"
              }
            },
            "cover": {
              "type": "string",
              "description": "封面"
            },
            "pageNumber": {
              "type": "number",
              "description": "文档页数"
            }
          }
        },
        "DocumentDto": {
          "type": "object",
          "properties": {
            "id": {
              "type": "number",
              "description": "id"
            },
            "uuid": {
              "type": "string",
              "description": "文档uuid"
            },
            "name": {
              "type": "string",
              "description": "文档名称"
            },
            "libraryId": {
              "type": "number",
              "description": "知识库id"
            },
            "folderId": {
              "type": "number",
              "description": "文件夹id"
            },
            "updateBy": {
              "type": "number",
              "description": "更新人id"
            },
            "status": {
              "type": "number",
              "description": "文档解析状态",
              "enum": [
                0,
                10,
                20,
                30,
                -1
              ]
            },
            "createTime": {
              "format": "date-time",
              "type": "string",
              "description": "创建时间"
            },
            "updateTime": {
              "format": "date-time",
              "type": "string",
              "description": "更新时间"
            },
            "extraData": {
              "description": "文档信息",
              "allOf": [
                {
                  "$ref": "#/components/schemas/DocumentExtraDataDto"
                }
              ]
            }
          },
          "required": [
            "id",
            "uuid",
            "name",
            "libraryId",
            "folderId",
            "updateBy",
            "status",
            "createTime",
            "updateTime",
            "extraData"
          ]
        },
        "CreateFianceDocumentDto": {
          "type": "object",
          "properties": {
            "file": {
              "type": "string",
              "description": "文档",
              "format": "binary"
            },
            "name": {
              "type": "string",
              "description": "文档名称"
            },
            "libraryId": {
              "type": "number",
              "description": "知识库id"
            },
            "company": {
              "type": "string",
              "description": "企业名称"
            },
            "financeDate": {
              "type": "date",
              "description": "财报时间"
            },
            "financeType": {
              "type": "string",
              "description": "财报类型"
            },
            "stockSymbol": {
              "type": "string",
              "description": "股票代码",
              "example": ""
            },
            "industry": {
              "description": "行业",
              "type": "array",
              "items": {
                "type": "string"
              }
            },
            "concept": {
              "description": "概念",
              "type": "array",
              "items": {
                "type": "string"
              }
            },
            "pageNumber": {
              "type": "number",
              "description": "文档页数"
            }
          },
          "required": [
            "file",
            "name",
            "libraryId",
            "company",
            "financeDate"
          ]
        },
        "PaginatedDto": {
          "type": "object",
          "properties": {
            "total": {
              "type": "number",
              "description": "total"
            }
          },
          "required": [
            "total"
          ]
        },
        "DocumentDtoDetailDto": {
          "type": "object",
          "properties": {
            "id": {
              "type": "number",
              "description": "id"
            },
            "uuid": {
              "type": "string",
              "description": "文档uuid"
            },
            "name": {
              "type": "string",
              "description": "文档名称"
            },
            "libraryId": {
              "type": "number",
              "description": "知识库id"
            },
            "folderId": {
              "type": "number",
              "description": "文件夹id"
            },
            "updateBy": {
              "type": "number",
              "description": "更新人id"
            },
            "status": {
              "type": "number",
              "description": "文档解析状态",
              "enum": [
                0,
                10,
                20,
                30,
                -1
              ]
            },
            "createTime": {
              "format": "date-time",
              "type": "string",
              "description": "创建时间"
            },
            "updateTime": {
              "format": "date-time",
              "type": "string",
              "description": "更新时间"
            },
            "extraData": {
              "description": "文档信息",
              "allOf": [
                {
                  "$ref": "#/components/schemas/DocumentExtraDataDto"
                }
              ]
            },
            "updateByName": {
              "type": "string",
              "description": "更新人account"
            }
          },
          "required": [
            "id",
            "uuid",
            "name",
            "libraryId",
            "folderId",
            "updateBy",
            "status",
            "createTime",
            "updateTime",
            "extraData",
            "updateByName"
          ]
        },
        "DocSortDto": {
          "type": "object",
          "properties": {
            "financeDate": {
              "type": "string",
              "enum": [
                "ASC",
                "DESC"
              ]
            },
            "updateTime": {
              "type": "string",
              "enum": [
                "ASC",
                "DESC"
              ]
            }
          },
          "required": [
            "financeDate",
            "updateTime"
          ]
        },
        "ListDocBodyDto": {
          "type": "object",
          "properties": {
            "libraryId": {
              "type": "number",
              "description": "知识库id",
              "default": 1
            },
            "financeDate": {
              "description": "财报时间",
              "example": [
                "2025-03-25T10:32:16.522Z",
                null
              ],
              "type": "array",
              "items": {
                "format": "date-time",
                "type": "string"
              }
            },
            "company": {
              "type": "string",
              "description": "企业名称",
              "default": ""
            },
            "financeType": {
              "description": "财报类型",
              "default": null,
              "type": "array",
              "items": {
                "type": "string"
              }
            },
            "industry": {
              "description": "行业",
              "default": null,
              "type": "array",
              "items": {
                "type": "string"
              }
            },
            "concept": {
              "description": "概念",
              "default": null,
              "type": "array",
              "items": {
                "type": "string"
              }
            },
            "name": {
              "type": "string",
              "description": "文档名称",
              "default": ""
            },
            "status": {
              "description": "状态",
              "example": [
                30
              ],
              "type": "array",
              "items": {
                "type": "number"
              }
            },
            "visibility": {
              "type": "object",
              "description": "可见",
              "example": 1
            },
            "updateBy": {
              "description": "更新人",
              "example": [
                1
              ],
              "type": "array",
              "items": {
                "type": "number"
              }
            },
            "updateTime": {
              "description": "更新时间",
              "example": [
                "2025-03-25T10:32:16.523Z",
                null
              ],
              "type": "array",
              "items": {
                "format": "date-time",
                "type": "string"
              }
            },
            "keywords": {
              "type": "string",
              "description": "文档名称&企业名称&财报时间&股票代码",
              "default": null
            },
            "page": {
              "type": "number",
              "example": 1
            },
            "pageSize": {
              "type": "number",
              "example": 10
            },
            "sort": {
              "description": "排序",
              "allOf": [
                {
                  "$ref": "#/components/schemas/DocSortDto"
                }
              ]
            }
          },
          "required": [
            "libraryId",
            "page",
            "pageSize"
          ]
        },
        "ListByFilterDto": {
          "type": "object",
          "properties": {
            "ids": {
              "description": "文档id集合",
              "type": "array",
              "items": {
                "type": "number"
              }
            },
            "uuids": {
              "description": "文档uuids集合",
              "type": "array",
              "items": {
                "type": "string"
              }
            },
            "folderIds": {
              "description": "文件夹id集合",
              "type": "array",
              "items": {
                "type": "number"
              }
            },
            "filename": {
              "type": "string",
              "description": "文档名称"
            },
            "status": {
              "type": "number",
              "description": "文档状态",
              "enum": [
                0,
                10,
                20,
                30,
                -1
              ]
            },
            "type": {
              "type": "number",
              "description": "文档类型",
              "enum": [
                0,
                1
              ]
            }
          }
        },
        "ListByUserDto": {
          "type": "object",
          "properties": {
            "userId": {
              "type": "number",
              "description": "用户id"
            },
            "name": {
              "type": "string",
              "description": "文档名称",
              "default": ""
            },
            "status": {
              "description": "状态",
              "example": [
                30
              ],
              "type": "array",
              "items": {
                "type": "number"
              }
            },
            "updateTime": {
              "description": "更新时间",
              "example": [
                "2025-03-25T10:32:16.525Z",
                null
              ],
              "type": "array",
              "items": {
                "format": "date-time",
                "type": "string"
              }
            }
          }
        },
        "DocIdListDto": {
          "type": "object",
          "properties": {
            "ids": {
              "description": "id集合",
              "type": "array",
              "items": {
                "type": "number"
              }
            }
          },
          "required": [
            "ids"
          ]
        },
        "DocumentFolderMoveDto": {
          "type": "object",
          "properties": {
            "documentId": {
              "type": "number",
              "description": "文档id"
            },
            "folderId": {
              "type": "number",
              "description": "文件夹id（移动到根目录时为null）"
            }
          },
          "required": [
            "documentId"
          ]
        },
        "UpdateDocDto": {
          "type": "object",
          "properties": {
            "id": {
              "type": "number",
              "description": "文档id"
            },
            "name": {
              "type": "string",
              "description": "文档名称"
            },
            "company": {
              "type": "string",
              "description": "企业名称",
              "example": null
            },
            "financeDate": {
              "format": "date-time",
              "type": "string",
              "description": "财报时间",
              "example": null
            },
            "financeType": {
              "type": "string",
              "description": "财报类型",
              "example": null
            },
            "stockSymbol": {
              "type": "string",
              "description": "股票代码",
              "example": null
            },
            "industry": {
              "description": "行业",
              "example": null,
              "type": "array",
              "items": {
                "type": "string"
              }
            },
            "concept": {
              "description": "概念",
              "example": null,
              "type": "array",
              "items": {
                "type": "string"
              }
            },
            "cover": {
              "type": "string",
              "description": "封面",
              "example": null
            },
            "pageNumber": {
              "type": "number",
              "description": "文档页数",
              "example": null
            },
            "documentSize": {
              "type": "number",
              "description": "文档大小",
              "example": null
            },
            "status": {
              "type": "number",
              "description": "状态",
              "example": null
            },
            "visibility": {
              "type": "number",
              "description": "状态",
              "example": null
            }
          },
          "required": [
            "id"
          ]
        },
        "DocumentSortDto": {
          "type": "object",
          "properties": {
            "id": {
              "type": "number",
              "description": "文档id"
            },
            "sort": {
              "type": "number",
              "description": "文档顺序"
            },
            "type": {
              "type": "string",
              "description": "类型（文档/文件夹）",
              "enum": [
                "folder",
                "document"
              ],
              "example": "document"
            }
          },
          "required": [
            "id",
            "sort",
            "type"
          ]
        },
        "FileMeta": {
          "type": "object",
          "properties": {
            "page_number": {
              "type": "number",
              "description": "文档总页数"
            },
            "first_image_id": {
              "type": "string",
              "description": "第一页图片ID"
            },
            "knowledge_id": {
              "type": "string",
              "description": "系统知识库：0，个人知识库：User_1（User_{user_id}）"
            },
            "ori_type": {
              "type": "string",
              "description": "文档所属（系统知识库、个人知识库）"
            }
          }
        },
        "CallbackDto": {
          "type": "object",
          "properties": {
            "uuid": {
              "type": "string",
              "description": "文档uuid"
            },
            "status": {
              "type": "number",
              "description": "状态(上传完成,docparser解析成功,目录解析成功,成功,失败)",
              "enum": [
                1,
                2,
                3,
                4,
                5,
                -1
              ]
            },
            "message": {
              "type": "string",
              "description": "信息"
            },
            "file_meta": {
              "description": "回调文档信息",
              "allOf": [
                {
                  "$ref": "#/components/schemas/FileMeta"
                }
              ]
            }
          },
          "required": [
            "uuid",
            "status",
            "file_meta"
          ]
        },
        "DocSummaryDto": {
          "type": "object",
          "properties": {
            "uuid": {
              "type": "string",
              "description": "文档uuid"
            },
            "data": {
              "type": "string",
              "description": "内容"
            },
            "id": {
              "type": "number",
              "description": "文档id"
            },
            "regeneration": {
              "type": "boolean",
              "description": "重新生成",
              "default": null
            }
          }
        },
        "FilterItem": {
          "type": "object",
          "properties": {
            "name": {
              "type": "string",
              "description": "名称"
            },
            "value": {
              "type": "string",
              "description": "值"
            }
          },
          "required": [
            "name",
            "value"
          ]
        },
        "FilterConfigDto": {
          "type": "object",
          "properties": {
            "financeType": {
              "description": "财报类型",
              "type": "array",
              "items": {
                "$ref": "#/components/schemas/FilterItem"
              }
            },
            "industry": {
              "description": "行业",
              "type": "array",
              "items": {
                "$ref": "#/components/schemas/FilterItem"
              }
            },
            "concept": {
              "description": "概念",
              "type": "array",
              "items": {
                "$ref": "#/components/schemas/FilterItem"
              }
            }
          },
          "required": [
            "financeType",
            "industry",
            "concept"
          ]
        },
        "ChatContentResDto": {
          "type": "object",
          "properties": {
            "id": {
              "type": "number"
            },
            "chatId": {
              "type": "number"
            },
            "content": {
              "type": "string",
              "description": "内容"
            },
            "type": {
              "type": "number",
              "enum": [
                1,
                2
              ],
              "description": "类型(1提问/2回答)"
            },
            "source": {
              "type": "string",
              "description": "来源信息"
            },
            "feedback": {
              "type": "number",
              "description": "反馈"
            },
            "createTime": {
              "format": "date-time",
              "type": "string"
            },
            "updateTime": {
              "format": "date-time",
              "type": "string"
            }
          },
          "required": [
            "id",
            "chatId",
            "content",
            "type",
            "source",
            "feedback",
            "createTime",
            "updateTime"
          ]
        },
        "CreateChatDto": {
          "type": "object",
          "properties": {
            "question": {
              "type": "string",
              "description": "提问内容",
              "example": "今年是哪一年"
            },
            "chatId": {
              "type": "number",
              "description": "对话id",
              "example": null
            },
            "documentIds": {
              "description": "文档id集合",
              "example": [
                1
              ],
              "type": "array",
              "items": {
                "type": "number"
              }
            },
            "folderIds": {
              "description": "文件夹id集合",
              "example": null,
              "type": "array",
              "items": {
                "type": "string"
              }
            },
            "stream": {
              "type": "boolean",
              "description": "stream流返回",
              "default": false
            },
            "ignore": {
              "type": "boolean",
              "description": "不显示对话记录",
              "default": false
            }
          },
          "required": [
            "question"
          ]
        },
        "CreateGlobalChatDto": {
          "type": "object",
          "properties": {
            "qaType": {
              "type": "string",
              "description": "提问类型",
              "example": "analyst"
            },
            "question": {
              "type": "string",
              "description": "提问内容",
              "example": "今年是哪一年"
            },
            "chatId": {
              "type": "number",
              "description": "对话id",
              "example": null
            },
            "stream": {
              "type": "boolean",
              "description": "stream流返回",
              "default": false
            },
            "ignore": {
              "type": "boolean",
              "description": "不显示对话记录",
              "default": false
            }
          },
          "required": [
            "qaType",
            "question"
          ]
        },
        "RecommendDto": {
          "type": "object",
          "properties": {
            "documentIds": {
              "description": "文档id集合",
              "type": "array",
              "items": {
                "type": "number"
              }
            }
          },
          "required": [
            "documentIds"
          ]
        },
        "ChatResDto": {
          "type": "object",
          "properties": {
            "id": {
              "type": "number"
            },
            "name": {
              "type": "string"
            },
            "context": {
              "type": "object"
            },
            "userId": {
              "type": "number"
            },
            "createTime": {
              "format": "date-time",
              "type": "string"
            },
            "updateTime": {
              "format": "date-time",
              "type": "string"
            }
          },
          "required": [
            "id",
            "name",
            "context",
            "userId",
            "createTime",
            "updateTime"
          ]
        },
        "AnswerIdsDto": {
          "type": "object",
          "properties": {
            "answerIds": {
              "description": "回答id集合",
              "type": "array",
              "items": {
                "type": "number"
              }
            },
            "questionIds": {
              "description": "提问id集合",
              "type": "array",
              "items": {
                "type": "number"
              }
            },
            "compatible": {
              "type": "boolean",
              "description": "兼容处理",
              "default": true
            }
          }
        },
        "FeedbackDto": {
          "type": "object",
          "properties": {
            "contentId": {
              "type": "number",
              "description": "内容id"
            },
            "feedback": {
              "type": "number",
              "description": "反馈(赞1/踩2)",
              "enum": [
                1,
                2
              ]
            }
          },
          "required": [
            "contentId",
            "feedback"
          ]
        },
        "UpdateChatDto": {
          "type": "object",
          "properties": {
            "chatId": {
              "type": "number",
              "description": "对话id"
            },
            "name": {
              "type": "string",
              "description": "对话标题"
            }
          },
          "required": [
            "chatId",
            "name"
          ]
        },
        "IdsChatDto": {
          "type": "object",
          "properties": {
            "ids": {
              "description": "对话id集合",
              "type": "array",
              "items": {
                "type": "number"
              }
            }
          },
          "required": [
            "ids"
          ]
        },
        "ChatContentListResDto": {
          "type": "object",
          "properties": {
            "id": {
              "type": "number"
            },
            "chatId": {
              "type": "number"
            },
            "content": {
              "type": "string",
              "description": "内容"
            },
            "type": {
              "type": "number",
              "enum": [
                1,
                2
              ],
              "description": "类型(1提问/2回答)"
            },
            "source": {
              "type": "string",
              "description": "来源信息"
            },
            "feedback": {
              "type": "number",
              "description": "反馈"
            },
            "createTime": {
              "format": "date-time",
              "type": "string"
            },
            "updateTime": {
              "format": "date-time",
              "type": "string"
            },
            "context": {
              "type": "object"
            },
            "documents": {
              "type": "array",
              "items": {
                "$ref": "#/components/schemas/DocumentDto"
              }
            }
          },
          "required": [
            "id",
            "chatId",
            "content",
            "type",
            "source",
            "feedback",
            "createTime",
            "updateTime",
            "context",
            "documents"
          ]
        },
        "QASortDto": {
          "type": "object",
          "properties": {
            "createTime": {
              "type": "string",
              "enum": [
                "ASC",
                "DESC"
              ]
            }
          },
          "required": [
            "createTime"
          ]
        },
        "ListChatBodyDto": {
          "type": "object",
          "properties": {
            "question": {
              "type": "string",
              "description": "问题"
            },
            "documentIds": {
              "description": "文档id集合",
              "type": "array",
              "items": {
                "type": "number"
              }
            },
            "complianceCheck": {
              "description": "合规审核状态集合",
              "type": "array",
              "items": {
                "type": "number"
              }
            },
            "createTime": {
              "description": "提问时间",
              "example": null,
              "type": "array",
              "items": {
                "format": "date-time",
                "type": "string"
              }
            },
            "userId": {
              "type": "number",
              "description": "用户id"
            },
            "chatType": {
              "type": "number",
              "description": "问答类型：1. 指定文档问答，2. 全局问答"
            },
            "full": {
              "type": "number",
              "description": "是否查询全部（后台搜索）"
            },
            "excludeInternalUser": {
              "type": "boolean",
              "description": "是否过滤内部用户"
            },
            "page": {
              "type": "number",
              "example": 1
            },
            "pageSize": {
              "type": "number",
              "example": 10
            },
            "sort": {
              "description": "排序",
              "allOf": [
                {
                  "$ref": "#/components/schemas/QASortDto"
                }
              ]
            }
          },
          "required": [
            "userId",
            "chatType",
            "full",
            "page",
            "pageSize"
          ]
        },
        "StatisticsResDto": {
          "type": "object",
          "properties": {
            "count": {
              "type": "number",
              "description": "总数"
            },
            "rangeTotal": {
              "type": "number",
              "description": "查询范围内的总数"
            },
            "list": {
              "description": "每天都调用数",
              "type": "array",
              "items": {
                "type": "string"
              }
            }
          },
          "required": [
            "count",
            "rangeTotal",
            "list"
          ]
        },
        "StatisticsDto": {
          "type": "object",
          "properties": {
            "createTime": {
              "description": "提问时间",
              "example": [
                "2025-03-25T10:32:17.143Z",
                "2025-03-25T10:32:17.143Z"
              ],
              "type": "array",
              "items": {
                "format": "date-time",
                "type": "string"
              }
            },
            "split": {
              "type": "string",
              "description": "统计维度",
              "enum": [
                "hour",
                "day"
              ]
            }
          },
          "required": [
            "createTime"
          ]
        },
        "RecycleItemDto": {
          "type": "object",
          "properties": {
            "id": {
              "type": "number"
            },
            "source": {
              "type": "object"
            },
            "expiry": {
              "format": "date-time",
              "type": "string"
            },
            "userId": {
              "type": "number"
            },
            "createTime": {
              "format": "date-time",
              "type": "string"
            }
          },
          "required": [
            "id",
            "source",
            "expiry",
            "userId",
            "createTime"
          ]
        },
        "RecycleListQueryDto": {
          "type": "object",
          "properties": {
            "name": {
              "type": "string",
              "description": "名称"
            },
            "type": {
              "type": "number",
              "description": "类型",
              "enum": [
                1,
                2,
                3
              ]
            },
            "sort": {
              "type": "string",
              "description": "排序",
              "enum": [
                "createTime",
                "name"
              ]
            },
            "sortType": {
              "type": "string",
              "description": "升序/降序",
              "enum": [
                "ASC",
                "DESC"
              ]
            }
          }
        },
        "RecycleIdListDto": {
          "type": "object",
          "properties": {
            "ids": {
              "description": "id集合",
              "type": "array",
              "items": {
                "type": "number"
              }
            }
          },
          "required": [
            "ids"
          ]
        },
        "UpdateConfigDto": {
          "type": "object",
          "properties": {
            "key": {
              "type": "string",
              "description": "key"
            },
            "data": {
              "type": "object",
              "description": "data"
            }
          },
          "required": [
            "key",
            "data"
          ]
        },
        "ISmsDto": {
          "type": "object",
          "properties": {
            "mobile": {
              "type": "string",
              "description": "手机号"
            },
            "mobileAreaCode": {
              "type": "string",
              "description": "国际区号",
              "example": "86"
            }
          },
          "required": [
            "mobile",
            "mobileAreaCode"
          ]
        },
        "GlobalSearchDto": {
          "type": "object",
          "properties": {
            "keywords": {
              "type": "string",
              "description": "keywords"
            }
          },
          "required": [
            "keywords"
          ]
        },
        "DocAllQueryDto": {
          "type": "object",
          "properties": {
            "ids": {
              "description": "id集合",
              "type": "array",
              "items": {
                "type": "number"
              }
            },
            "uuids": {
              "description": "uuid集合",
              "type": "array",
              "items": {
                "type": "string"
              }
            },
            "company": {
              "type": "string",
              "description": "公司"
            },
            "filename": {
              "type": "string",
              "description": "文件名"
            },
            "type": {
              "type": "number",
              "description": "类型",
              "enum": [
                0,
                1
              ],
              "example": null
            },
            "status": {
              "type": "number",
              "description": "状态"
            },
            "financeDate": {
              "description": "财报时间",
              "example": [
                "2025-03-25T10:32:17.168Z",
                null
              ],
              "type": "array",
              "items": {
                "format": "date-time",
                "type": "string"
              }
            },
            "financeType": {
              "description": "财报类型",
              "default": null,
              "type": "array",
              "items": {
                "type": "string"
              }
            },
            "pageNumber": {
              "description": "文档页数",
              "default": null,
              "type": "array",
              "items": {
                "type": "string"
              }
            }
          }
        },
        "SpotsDetailDto": {
          "type": "object",
          "properties": {
            "companies": {
              "description": "热门公司全称",
              "type": "array",
              "items": {
                "type": "string"
              }
            },
            "alias": {
              "description": "热门公司简称",
              "type": "array",
              "items": {
                "type": "string"
              }
            }
          }
        },
        "HotspotsDetailDto": {
          "type": "object",
          "properties": {
            "id": {
              "type": "number"
            },
            "createTime": {
              "format": "date-time",
              "type": "string"
            },
            "updateTime": {
              "format": "date-time",
              "type": "string"
            },
            "spots": {
              "description": "热点信息",
              "allOf": [
                {
                  "$ref": "#/components/schemas/SpotsDetailDto"
                }
              ]
            }
          },
          "required": [
            "id",
            "createTime",
            "updateTime",
            "spots"
          ]
        }
      }
    }
  },
  "customOptions": {}
};
  url = options.swaggerUrl || url
  let urls = options.swaggerUrls
  let customOptions = options.customOptions
  let spec1 = options.swaggerDoc
  let swaggerOptions = {
    spec: spec1,
    url: url,
    urls: urls,
    dom_id: '#swagger-ui',
    deepLinking: true,
    presets: [
      SwaggerUIBundle.presets.apis,
      SwaggerUIStandalonePreset
    ],
    plugins: [
      SwaggerUIBundle.plugins.DownloadUrl
    ],
    layout: "StandaloneLayout"
  }
  for (let attrname in customOptions) {
    swaggerOptions[attrname] = customOptions[attrname];
  }
  let ui = SwaggerUIBundle(swaggerOptions)

  if (customOptions.initOAuth) {
    ui.initOAuth(customOptions.initOAuth)
  }

  if (customOptions.authAction) {
    ui.authActions.authorize(customOptions.authAction)
  }
  
  window.ui = ui
}
