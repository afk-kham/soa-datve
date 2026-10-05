"use strict";
const test = require("node:test");
const assert = require("node:assert/strict");
const { normalizeTransaction, validateShape } = require("./payment_service");
test("valid PAID transaction uses numeric bookingId", () => { const t = normalizeTransaction({ bookingId: 3, amount: 180000, method: "momo" }); assert.equal(t.bookingId, 3); assert.equal(typeof t.bookingId, "number"); assert.equal(t.method, "MOMO"); assert.equal(t.status, "PAID"); assert.ok(t.paidAt instanceof Date); });
test("zero or negative amount is FAILED", () => { assert.equal(normalizeTransaction({ bookingId: 4, amount: 0, method: "MOMO" }).status, "FAILED"); assert.equal(normalizeTransaction({ bookingId: 5, amount: -1, method: "CASH" }).status, "FAILED"); });
test("unknown method is FAILED", () => { const t = normalizeTransaction({ bookingId: 6, amount: 100000, method: "BANK" }); assert.equal(t.status, "FAILED"); assert.equal(t.method, "BANK"); });
test("shape validation rejects malformed fields", () => { assert.match(validateShape({ bookingId: "3", amount: 1, method: "MOMO" }), /bookingId/); assert.match(validateShape({ bookingId: 3, method: "MOMO" }), /amount/); assert.match(validateShape({ bookingId: 3, amount: 1 }), /method/); assert.equal(validateShape({ bookingId: 3, amount: 1, method: "MOMO" }), null); });
