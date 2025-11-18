import express from "express";
import passport from 'passport';
import { forwardAuthenticated } from "../middleware/checkAuth";

const router = express.Router();

declare module "express-session" {
  interface SessionData {
    messages: string[];
  }
}

router.get("/github",
  passport.authenticate('github', { scope: ['user:email'] }));

router.get("/github/callback",
  passport.authenticate('github', { successRedirect: "/dashboard", failureRedirect: '/auth/login' }),
  function (req, res) {
    // Successful authentication, redirect home.
    res.redirect('/');
  });


router.get("/login", forwardAuthenticated, (req, res) => {
  const messages = req.session.messages || [];
  const errorMessage = messages[messages.length - 1] || null;
  req.session.messages = []; // clear after use
  res.render("login", { errorMessage });
})

router.post(
  "/login",
  passport.authenticate("local", {
    successRedirect: "/dashboard",
    failureRedirect: "/auth/login",
    failureMessage: true,
  })
);

router.get("/logout", (req, res) => {
  req.logout((err) => {
    if (err) console.log(err);
  });
  res.redirect("/auth/login");
});

export default router;
