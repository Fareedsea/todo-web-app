---
name: auth-skill
description: Implement secure authentication systems including signup, signin, password hashing, JWT tokens, and Better Auth integration.
---

# Authentication Skill

## Instructions

1. **User Signup**
   - Validate user input (email, password)
   - Hash passwords securely
   - Store user credentials safely
   - Prevent duplicate accounts

2. **User Signin**
   - Verify credentials against stored hashes
   - Handle invalid login attempts
   - Return authentication tokens on success

3. **Password Security**
   - Use strong hashing algorithms (bcrypt, argon2)
   - Apply salting and proper cost factors
   - Never store plain-text passwords

4. **JWT Authentication**
   - Generate access tokens on login
   - Include user claims securely
   - Set token expiration
   - Verify tokens on protected routes

5. **Better Auth Integration**
   - Configure Better Auth provider
   - Connect with database adapters
   - Enable session and token management
   - Support refresh tokens and logout

## Best Practices
- Enforce strong password policies
- Use HTTPS for all auth routes
- Store JWTs securely (httpOnly cookies preferred)
- Implement token expiration and rotation
- Rate-limit authentication endpoints
- Log authentication events carefully (no sensitive data)

## Example Structure
```js
// Signup
app.post("/signup", async (req, res) => {
  const hashedPassword = await bcrypt.hash(req.body.password, 12)
  await db.user.create({
    email: req.body.email,
    password: hashedPassword
  })
  res.status(201).send("User created")
})

// Signin
app.post("/signin", async (req, res) => {
  const user = await db.user.findUnique({ where: { email: req.body.email } })
  const isValid = await bcrypt.compare(req.body.password, user.password)

  if (!isValid) return res.status(401).send("Invalid credentials")

  const token = jwt.sign({ id: user.id }, process.env.JWT_SECRET, {
    expiresIn: "1h"
  })

  res.json({ token })
})
