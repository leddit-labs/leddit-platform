
    const schema = {
  "asyncapi": "3.0.0",
  "info": {
    "title": "Leddit Event Bus API",
    "version": "1.0.0",
    "description": "AsyncAPI documentation for all RabbitMQ message communication\nbetween Leddit microservices.\n"
  },
  "servers": {
    "rabbitmq": {
      "host": "rabbitmq:5672",
      "protocol": "amqp",
      "description": "RabbitMQ broker"
    }
  },
  "defaultContentType": "application/json",
  "channels": {
    "post.created": {
      "address": "post_created",
      "messages": {
        "postCreated": {
          "name": "post_created",
          "title": "Post Created Event",
          "payload": {
            "type": "object",
            "required": [
              "u_id",
              "community_id",
              "author_id",
              "title",
              "content"
            ],
            "properties": {
              "u_id": {
                "type": "string",
                "format": "uuid",
                "x-parser-schema-id": "<anonymous-schema-1>"
              },
              "community_id": {
                "type": "string",
                "format": "uuid",
                "x-parser-schema-id": "<anonymous-schema-2>"
              },
              "author_id": {
                "type": "string",
                "format": "uuid",
                "x-parser-schema-id": "<anonymous-schema-3>"
              },
              "title": {
                "type": "string",
                "x-parser-schema-id": "<anonymous-schema-4>"
              },
              "content": {
                "type": "string",
                "x-parser-schema-id": "<anonymous-schema-5>"
              }
            },
            "x-parser-schema-id": "PostCreatedPayload"
          },
          "x-parser-unique-object-id": "postCreated"
        }
      },
      "x-parser-unique-object-id": "post.created"
    },
    "post.updated": {
      "address": "post_updated",
      "messages": {
        "postUpdated": {
          "name": "post_updated",
          "title": "Post Updated Event",
          "payload": "$ref:$.channels.post.created.messages.postCreated.payload",
          "x-parser-unique-object-id": "postUpdated"
        }
      },
      "x-parser-unique-object-id": "post.updated"
    },
    "post.deleted": {
      "address": "post_deleted",
      "messages": {
        "postDeleted": {
          "name": "post_deleted",
          "title": "Post Deleted Event",
          "payload": {
            "type": "object",
            "properties": {
              "u_id": {
                "type": "string",
                "format": "uuid",
                "x-parser-schema-id": "<anonymous-schema-7>"
              }
            },
            "x-parser-schema-id": "<anonymous-schema-6>"
          },
          "x-parser-unique-object-id": "postDeleted"
        }
      },
      "x-parser-unique-object-id": "post.deleted"
    },
    "post.accepted": {
      "address": "post_accepted",
      "messages": {
        "postAccepted": {
          "name": "post_accepted",
          "payload": {
            "type": "object",
            "properties": {
              "u_id": {
                "type": "string",
                "x-parser-schema-id": "<anonymous-schema-9>"
              },
              "community_id": {
                "type": "string",
                "x-parser-schema-id": "<anonymous-schema-10>"
              },
              "author_id": {
                "type": "string",
                "x-parser-schema-id": "<anonymous-schema-11>"
              },
              "title": {
                "type": "string",
                "x-parser-schema-id": "<anonymous-schema-12>"
              }
            },
            "x-parser-schema-id": "<anonymous-schema-8>"
          },
          "x-parser-unique-object-id": "postAccepted"
        }
      },
      "x-parser-unique-object-id": "post.accepted"
    },
    "post.denied": {
      "address": "post_denied",
      "messages": {
        "postDenied": {
          "name": "post_denied",
          "payload": {
            "type": "object",
            "properties": {
              "u_id": {
                "type": "string",
                "x-parser-schema-id": "<anonymous-schema-14>"
              },
              "community_id": {
                "type": "string",
                "x-parser-schema-id": "<anonymous-schema-15>"
              },
              "author_id": {
                "type": "string",
                "x-parser-schema-id": "<anonymous-schema-16>"
              },
              "title": {
                "type": "string",
                "x-parser-schema-id": "<anonymous-schema-17>"
              }
            },
            "x-parser-schema-id": "<anonymous-schema-13>"
          },
          "x-parser-unique-object-id": "postDenied"
        }
      },
      "x-parser-unique-object-id": "post.denied"
    },
    "community.created": {
      "address": "community.created",
      "messages": {
        "communityCreated": {
          "name": "community.created",
          "payload": {
            "type": "object",
            "properties": {
              "community_id": {
                "type": "string",
                "x-parser-schema-id": "<anonymous-schema-18>"
              },
              "name": {
                "type": "string",
                "x-parser-schema-id": "<anonymous-schema-19>"
              },
              "description": {
                "type": "string",
                "x-parser-schema-id": "<anonymous-schema-20>"
              },
              "created_by": {
                "type": "string",
                "x-parser-schema-id": "<anonymous-schema-21>"
              }
            },
            "x-parser-schema-id": "CommunityPayload"
          },
          "x-parser-unique-object-id": "communityCreated"
        }
      },
      "x-parser-unique-object-id": "community.created"
    },
    "community.updated": {
      "address": "community_updated",
      "messages": {
        "communityUpdated": {
          "name": "community_updated",
          "payload": "$ref:$.channels.community.created.messages.communityCreated.payload",
          "x-parser-unique-object-id": "communityUpdated"
        }
      },
      "x-parser-unique-object-id": "community.updated"
    },
    "community.deleted": {
      "address": "community_deleted",
      "messages": {
        "communityDeleted": {
          "name": "community_deleted",
          "payload": {
            "type": "object",
            "properties": {
              "u_id": {
                "type": "string",
                "x-parser-schema-id": "<anonymous-schema-23>"
              }
            },
            "x-parser-schema-id": "<anonymous-schema-22>"
          },
          "x-parser-unique-object-id": "communityDeleted"
        }
      },
      "x-parser-unique-object-id": "community.deleted"
    },
    "vote.post.changed": {
      "address": "vote.post.changed",
      "messages": {
        "votePostChanged": {
          "name": "vote.post.changed",
          "payload": {
            "type": "object",
            "required": [
              "post_id",
              "user_id",
              "new_value"
            ],
            "properties": {
              "post_id": {
                "type": "string",
                "x-parser-schema-id": "<anonymous-schema-25>"
              },
              "user_id": {
                "type": "string",
                "x-parser-schema-id": "<anonymous-schema-26>"
              },
              "new_value": {
                "type": "integer",
                "x-parser-schema-id": "<anonymous-schema-27>"
              }
            },
            "x-parser-schema-id": "<anonymous-schema-24>"
          },
          "x-parser-unique-object-id": "votePostChanged"
        }
      },
      "x-parser-unique-object-id": "vote.post.changed"
    },
    "vote.comment.changed": {
      "address": "vote.comment.changed",
      "messages": {
        "voteCommentChanged": {
          "name": "vote.comment.changed",
          "payload": {
            "type": "object",
            "required": [
              "comment_id",
              "user_id",
              "new_value"
            ],
            "properties": {
              "comment_id": {
                "type": "string",
                "x-parser-schema-id": "<anonymous-schema-29>"
              },
              "user_id": {
                "type": "string",
                "x-parser-schema-id": "<anonymous-schema-30>"
              },
              "new_value": {
                "type": "integer",
                "x-parser-schema-id": "<anonymous-schema-31>"
              }
            },
            "x-parser-schema-id": "<anonymous-schema-28>"
          },
          "x-parser-unique-object-id": "voteCommentChanged"
        }
      },
      "x-parser-unique-object-id": "vote.comment.changed"
    }
  },
  "operations": {
    "publishPostCreated": {
      "action": "send",
      "channel": "$ref:$.channels.post.created",
      "summary": "Post service publishes new posts",
      "x-parser-unique-object-id": "publishPostCreated"
    },
    "consumePostCreated": {
      "action": "receive",
      "channel": "$ref:$.channels.post.created",
      "summary": "Integrity service consumes created posts",
      "x-parser-unique-object-id": "consumePostCreated"
    },
    "publishCommunityCreated": {
      "action": "send",
      "channel": "$ref:$.channels.community.created",
      "x-parser-unique-object-id": "publishCommunityCreated"
    },
    "consumeVotePostChanged": {
      "action": "receive",
      "channel": "$ref:$.channels.vote.post.changed",
      "x-parser-unique-object-id": "consumeVotePostChanged"
    },
    "consumeVoteCommentChanged": {
      "action": "receive",
      "channel": "$ref:$.channels.vote.comment.changed",
      "x-parser-unique-object-id": "consumeVoteCommentChanged"
    }
  },
  "components": {
    "messages": {
      "PostCreated": "$ref:$.channels.post.created.messages.postCreated",
      "PostUpdated": "$ref:$.channels.post.updated.messages.postUpdated",
      "PostDeleted": "$ref:$.channels.post.deleted.messages.postDeleted",
      "PostAccepted": "$ref:$.channels.post.accepted.messages.postAccepted",
      "PostDenied": "$ref:$.channels.post.denied.messages.postDenied",
      "CommunityCreated": "$ref:$.channels.community.created.messages.communityCreated",
      "CommunityUpdated": "$ref:$.channels.community.updated.messages.communityUpdated",
      "CommunityDeleted": "$ref:$.channels.community.deleted.messages.communityDeleted",
      "VotePostChanged": "$ref:$.channels.vote.post.changed.messages.votePostChanged",
      "VoteCommentChanged": "$ref:$.channels.vote.comment.changed.messages.voteCommentChanged"
    },
    "schemas": {
      "PostCreatedPayload": "$ref:$.channels.post.created.messages.postCreated.payload",
      "CommunityPayload": "$ref:$.channels.community.created.messages.communityCreated.payload"
    }
  },
  "x-parser-spec-parsed": true,
  "x-parser-api-version": 3,
  "x-parser-spec-stringified": true
};
    const config = {"show":{"sidebar":true},"sidebar":{"showOperations":"byDefault"}};
    const appRoot = document.getElementById('root');
    AsyncApiStandalone.render(
        { schema, config, }, appRoot
    );
  