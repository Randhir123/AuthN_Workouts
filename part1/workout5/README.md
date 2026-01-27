# Workout 5 — What Are We Actually Protecting?

There is no code in this workout.

That is intentional.

Up to this point, we have built a backend, a client, and a protected endpoint that rejects requests by default. We have made an authentication decision explicit, but we have not yet defined **what that decision means**. This workout exists to do exactly that.

Authentication does not protect endpoints.  
Authentication protects **actions and their consequences**.

Before adding tokens, identities, or protocols, we must be clear about what accepting a request actually allows someone to do.

---

## What this workout is about

This workout asks you to stop implementing mechanisms and instead define the **security meaning** of the protected endpoint.

You should be able to answer, in plain language:

- What action does this endpoint represent?
- What happens if an unauthorized request is accepted?
- Is the damage reversible or irreversible?
- Is the risk financial, operational, or regulatory?
- Is this action user-scoped, system-scoped, or global?

If you cannot answer these questions, any authentication mechanism you add next will be arbitrary.

---

## What we are not doing here

This workout intentionally does not introduce tokens, identities, OAuth, or an Identity Provider.

Those mechanisms only make sense once the protected action and its consequences are clearly defined. This step exists to establish that definition before any authentication technology is added.

---

## What you should do in this workout

For the protected endpoint you introduced earlier, write down (in comments, notes, or documentation):

1. **The action being protected**  
   For example: transferring funds, modifying configuration, triggering a job, reading sensitive data.

2. **The impact of a bad decision**  
   What is the worst-case outcome if an attacker can call this endpoint?

3. **What must be proven to accept the request**  
   Not *how* yet, just *what*. For example:  
   “The caller must present a verifiable assertion that they are allowed to perform this action at this time.”

4. **Any assumptions you are making**  
   For example: “Only internal callers will reach this endpoint.”  
   If an assumption cannot be enforced, it is not a security guarantee.

---

## Why this step matters

Most authentication systems fail not because a protocol was implemented incorrectly, but because the system never clearly defined what it was trying to protect.

If you skip this step, you will later struggle with questions like:

- What claims should go into the token?
- Do we need MFA here?
- How long should tokens live?
- Should this be user-based or service-based authentication?

This workout creates the anchor that makes those decisions principled instead of guesswork.

---

## Outcome of this workout

By the end of this step, you should have:

- a clear definition of the protected action
- an understanding of the risk involved
- a statement of what must be proven for a request to be accepted

Only after that does it make sense to introduce tokens and identity.

---

## One guiding idea

Authentication begins the moment a system decides whether to accept or reject an action.

Identity comes later.
