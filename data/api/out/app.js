"use strict";
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
var __generator = (this && this.__generator) || function (thisArg, body) {
    var _ = { label: 0, sent: function() { if (t[0] & 1) throw t[1]; return t[1]; }, trys: [], ops: [] }, f, y, t, g;
    return g = { next: verb(0), "throw": verb(1), "return": verb(2) }, typeof Symbol === "function" && (g[Symbol.iterator] = function() { return this; }), g;
    function verb(n) { return function (v) { return step([n, v]); }; }
    function step(op) {
        if (f) throw new TypeError("Generator is already executing.");
        while (_) try {
            if (f = 1, y && (t = op[0] & 2 ? y["return"] : op[0] ? y["throw"] || ((t = y["return"]) && t.call(y), 0) : y.next) && !(t = t.call(y, op[1])).done) return t;
            if (y = 0, t) op = [op[0] & 2, t.value];
            switch (op[0]) {
                case 0: case 1: t = op; break;
                case 4: _.label++; return { value: op[1], done: false };
                case 5: _.label++; y = op[1]; op = [0]; continue;
                case 7: op = _.ops.pop(); _.trys.pop(); continue;
                default:
                    if (!(t = _.trys, t = t.length > 0 && t[t.length - 1]) && (op[0] === 6 || op[0] === 2)) { _ = 0; continue; }
                    if (op[0] === 3 && (!t || (op[1] > t[0] && op[1] < t[3]))) { _.label = op[1]; break; }
                    if (op[0] === 6 && _.label < t[1]) { _.label = t[1]; t = op; break; }
                    if (t && _.label < t[2]) { _.label = t[2]; _.ops.push(op); break; }
                    if (t[2]) _.ops.pop();
                    _.trys.pop(); continue;
            }
            op = body.call(thisArg, _);
        } catch (e) { op = [6, e]; y = 0; } finally { f = t = 0; }
        if (op[0] & 5) throw op[1]; return { value: op[0] ? op[1] : void 0, done: true };
    }
};
var __importStar = (this && this.__importStar) || function (mod) {
    if (mod && mod.__esModule) return mod;
    var result = {};
    if (mod != null) for (var k in mod) if (Object.hasOwnProperty.call(mod, k)) result[k] = mod[k];
    result["default"] = mod;
    return result;
};
Object.defineProperty(exports, "__esModule", { value: true });
// importing the dependencies
var express = require("express");
var helmet = require("helmet");
var cors = require("cors");
var morgan = require("morgan");
var sqlite3 = require("sqlite3");
var config = __importStar(require("./config/config.json"));
var path = require('path');
var db = new sqlite3.Database('./../db/db.bin');
var app = express();
app.use(helmet());
app.use(cors());
app.use(morgan('combined'));
app.use(express.static('search'));
app.get('/', function (req, res) {
    res.send("hello");
});
app.get('/getresults', function (req, res) { return __awaiter(void 0, void 0, void 0, function () {
    var _a, _b;
    return __generator(this, function (_c) {
        switch (_c.label) {
            case 0:
                _b = (_a = res).send;
                return [4 /*yield*/, getStateResults()];
            case 1:
                _b.apply(_a, [_c.sent()]);
                return [2 /*return*/];
        }
    });
}); });
app.post('/insertpoll', function (req, res) { return __awaiter(void 0, void 0, void 0, function () {
    var state, demVotes, repVotes, demProb, repProb, date, notes;
    return __generator(this, function (_a) {
        console.log("INSERTING POLL");
        state = req.query.state;
        demVotes = req.query.demVotes;
        repVotes = req.query.repVotes;
        demProb = req.query.demProb;
        repProb = req.query.repProb;
        date = req.query.date;
        notes = req.query.notes;
        insertPoll(state, demVotes, repVotes, demProb, repProb, date, notes);
        res.send('OK');
        return [2 /*return*/];
    });
}); });
app.listen(config.port, function () {
    console.log('listening on port ' + config.port);
});
app.post('/postthread', function (req, res) { return __awaiter(void 0, void 0, void 0, function () {
    var query, data, prom, updateQuery;
    return __generator(this, function (_a) {
        switch (_a.label) {
            case 0:
                query = "SELECT * FROM DATA WHERE STATUS='RECORDED' AND DATA <>'[removed]' AND DATA <> '[deleted]' ORDER BY RANDOM() DESC LIMIT 1";
                data = {};
                return [4 /*yield*/, new Promise(function (resolve, reject) {
                        db.all(query, function (err, rows) {
                            var _this = this;
                            rows.forEach(function (row) { return __awaiter(_this, void 0, void 0, function () {
                                return __generator(this, function (_a) {
                                    data = row;
                                    return [2 /*return*/];
                                });
                            }); });
                            resolve(data);
                        });
                    })];
            case 1:
                prom = _a.sent();
                updateQuery = "UPDATE DATA SET STATUS='POSTED' WHERE ID=?";
                db.run(updateQuery, [data['ID']], function (err) {
                });
                return [2 /*return*/];
        }
    });
}); });
function getStateResults() {
    return __awaiter(this, void 0, void 0, function () {
        var query, data, prom;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0:
                    query = "SELECT * FROM V_POLLS";
                    data = {};
                    return [4 /*yield*/, new Promise(function (resolve, reject) {
                            db.all(query, function (err, rows) {
                                rows.forEach(function (row) {
                                    if (row['PROB_A'] === row['PROB_B'])
                                        row.result = 0;
                                    else {
                                        row.result = row['PROB_A'] > row['PROB_B'] ? 1 : -1;
                                    }
                                });
                                resolve(rows);
                            });
                        })];
                case 1:
                    prom = _a.sent();
                    return [2 /*return*/, prom];
            }
        });
    });
}
function insertPoll(state, votes_a, votes_b, prob_a, prob_b, curDate, notes) {
    return __awaiter(this, void 0, void 0, function () {
        var query;
        return __generator(this, function (_a) {
            query = "INSERT OR REPLACE INTO POLLS (\"STATE\", \"VOTES_A\", \"VOTES_B\", \"PROB_A\", \"PROB_B\", \"DATE\", \"NOTES\") VALUES (?, ?, ?, ?, ?, ?, ?)";
            db.run(query, [state, votes_a, votes_b, prob_a, prob_b, curDate, notes], function (err) {
                console.log(err);
            });
            return [2 /*return*/];
        });
    });
}
//# sourceMappingURL=app.js.map