"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const express_1 = __importDefault(require("express"));
const router = express_1.default.Router();
const checkAuth_1 = require("../middleware/checkAuth");
router.get("/", (req, res) => {
    res.send("welcome");
});
router.get("/dashboard", checkAuth_1.ensureAuthenticated, (req, res) => {
    res.render("dashboard", {
        user: req.user,
    });
});
exports.default = router;
