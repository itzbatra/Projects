import express from "express";
import { ensureAdminAuth } from "../middleware/checkAuth";

const adminRouter = express.Router();

adminRouter.get("/", ensureAdminAuth, (req, res) => {
    (req.sessionStore as any).all((err: any, sessions: Record<string, any>) => {
        if (err) return res.status(500).send(err.message);
        res.render("admin", { sessions });
    });
});

adminRouter.post(
    "/revoke/:sid",
    ensureAdminAuth,
    (req, res) => {
        req.sessionStore.destroy(req.params.sid, (err: any) => {
            if (err) return res.status(500).send(err.message);
            res.redirect("/admin");
        });
    }
);

export default adminRouter;