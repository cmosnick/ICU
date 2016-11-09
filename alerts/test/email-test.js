var expect = require('chai').expect;
var supertest = require('supertest');

var app = require('../server');
var config = require('../config');

describe('Email sent successfully', function() {
  var agent = supertest(app);

  describe('GET /emailUser', function() {
    it('should not return an error; email sent successfully', function(done) {
      agent
        .get('/emailUser?toEmail=jamestapia54@gmail.com')
        .expect(function(res) {
          expect(res.status).to.equal(200);
        })
        .end(done);
    });
  });
});
