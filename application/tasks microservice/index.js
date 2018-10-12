'use strict';

const tasksdb = require('./tasksdb.json');

const createResponse = (statusCode, body) => {

    return {
        statusCode: statusCode,
        body: body
    }
};


exports.handler = function(event, context, callback) {

      console.log(event);
      console.log(event["pathParameters"]["proxy"]);

      if(event["pathParameters"]["proxy"].startsWith('api/tasks/by-user/'))
      {
        var strings =  event["pathParameters"]["proxy"].split('/');
        callback(null, createResponse(200, JSON.stringify(tasksdb.tasks.filter((task) => task.user == strings[3]))));

      }
      else if(event["pathParameters"]["proxy"].startsWith('api/tasks'))
      {
         if(event['httpMethod'] == 'GET')
         {
            if(event["pathParameters"]["proxy"] == 'api/tasks')
            {
                callback(null, createResponse(200, JSON.stringify(tasksdb.tasks)));
            }
            else
            {
                var strings =  event["pathParameters"]["proxy"].split('/');
                callback(null, createResponse(200, JSON.stringify(tasksdb.tasks.filter((task) => task.id == strings[2]))));
            }
         }
         else if(event['httpMethod'] == 'PUT')
         {
            callback(null, createResponse(200, 'Task Put Successfully'));
         }
      }
}