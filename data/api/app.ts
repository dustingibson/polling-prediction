// importing the dependencies
import express = require('express');
import helmet = require('helmet');
import cors = require('cors');
import morgan = require('morgan');
import sqlite3 = require('sqlite3');
import * as config from './config/config.json';
import { resolve } from 'url';
import { REPLServer } from 'repl';
var path = require('path');


let db = new sqlite3.Database('./../db/db.bin');

const app = express();

app.use(helmet());

app.use(cors());

app.use(morgan('combined'));

app.use(express.static('search'))

app.get('/', (req, res) => {
  res.send("hello");
});

app.get('/getresults', async (req, res) => {
  res.send(await getStateResults());
});

app.post('/insertpoll', async (req, res) => {
  console.log("INSERTING POLL"); 
  const state = req.query.state;
  const demVotes = req.query.demVotes;
  const repVotes = req.query.repVotes;
  const demProb = req.query.demProb;
  const repProb = req.query.repProb;
  const date = req.query.date;
  const notes = req.query.notes;
  insertPoll(state, demVotes, repVotes, demProb, repProb, date, notes);
  res.send('OK');
});

app.listen(config.port, () => {
    console.log('listening on port ' + config.port);
  });

app.post('/postthread', async (req, res) => {
  const query = "SELECT * FROM DATA WHERE STATUS='RECORDED' AND DATA <>'[removed]' AND DATA <> '[deleted]' ORDER BY RANDOM() DESC LIMIT 1";
  let data = {};
  const prom = await new Promise(function (resolve, reject) {
  db.all(query, function(err, rows) {
      rows.forEach( async (row) => { 
        data = row;
      });
      resolve(data);
    })
  });
  const updateQuery = `UPDATE DATA SET STATUS='POSTED' WHERE ID=?`;
  db.run(updateQuery, [data['ID']], function(err) {
  });
});

async function getStateResults() {
    //TODO: Cache results
    const query = `SELECT * FROM V_POLLS`;
    let data = {};
    const prom = await new Promise(function (resolve, reject) {
      db.all(query, function(err, rows) {
        rows.forEach( (row) => {
          if(row['PROB_A'] === row['PROB_B'])
            row.result = 0;
          else {
            row.result = row['PROB_A'] > row['PROB_B'] ? 1 : -1;
          }
        });
        resolve(rows);
      });
    });
    return prom;
}

async function insertPoll(state, votes_a, votes_b, prob_a, prob_b, curDate, notes ) {
  let query = `INSERT OR REPLACE INTO POLLS ("STATE", "VOTES_A", "VOTES_B", "PROB_A", "PROB_B", "DATE", "NOTES") VALUES (?, ?, ?, ?, ?, ?, ?)`;
  db.run(query, [state, votes_a, votes_b, prob_a, prob_b, curDate, notes], function(err) {
    console.log(err);
  });
}