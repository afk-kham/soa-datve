// Chạy: mongosh < seed.js
use("payment_db");
db.transactions.deleteMany({});
db.transactions.insertMany([
  { bookingId: 1, amount: 180000, method: "MOMO", status: "PAID", paidAt: ISODate("2026-10-01T10:00:00Z") },
  { bookingId: 2, amount: 85000, method: "VNPAY", status: "FAILED", paidAt: ISODate("2026-10-01T10:05:00Z") }
]);
db.transactions.createIndex({ bookingId: 1 });
printjson(db.transactions.find({}, { _id: 0 }).sort({ paidAt: 1 }).toArray());
