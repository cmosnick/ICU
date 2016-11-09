var expect = require('chai').expect;
var supertest = require('supertest');

var app = require('../server');
var config = require('../config');

describe('Message sent successfully', function() {
  var agent = supertest(app);

  describe('GET /sendSMS', function() {
    it('should not return an error; message sent successfully', function(done) {
      agent
        .get('/sendSMS?toNum=+16362299752&text=BRUHHHH&image=http://vignette3.wikia.nocookie.net/simpsons/images/e/e9/Nelson_Ha-Ha.jpg/revision/latest?cb=20121205194057')
        .expect(function(res) {
          expect(res.status).to.equal(200);
        })
        .end(done);
    });
  });
});
