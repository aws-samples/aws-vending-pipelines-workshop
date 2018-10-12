const app = require('koa')();
const router = require('koa-router')();
const db = require('./db.json');

// Log requests
app.use(function *(next){
  const start = new Date;
  yield next;
  const ms = new Date - start;
  console.log('%s %s - %s', this.method, this.url, ms);
});

router.get('/api/tasks/:taskId', function *() {
  const id = parseInt(this.params.taskId);
  this.body = db.tasks.filter((task) => task.id == id);
});

router.get('/api/tasks/', function *() {
  this.body = db.tasks;
});

router.get('/api/tasks/by-user/:userId', function *() {
  const id = parseInt(this.params.userId);
  this.body = db.tasks.filter((task) => task.user == id);
});

router.get('/api/', function *() {
  this.body = "API ready to receive requests";
});

router.get('/', function *() {
  this.body = "Ready to receive requests";
});

app.use(router.routes());
app.use(router.allowedMethods());

app.listen(3000);

console.log('Worker started');
