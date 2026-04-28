# Question 15

> **Solve this question on:** `ckad-lab-15`

Perform the following Custom Resource Definition tasks:

1. Create a CRD for an `Operator` resource with the following specification:
   - API group: `stable.example.com`, version: `v1`
   - Names: plural=`operators`, singular=`operator`, shortName=`op`, kind=`Operator`
   - Scope: `Namespaced`
   - Schema: required string fields `email` and `name`; required integer field `age`

2. Once the CRD is established, create a custom `Operator` resource named `operator-sample` in namespace `default` with:
   - `email: operator-sample@stable.example.com`
   - `name: operator sample`
   - `age: 30`

3. Verify the resource can be listed using all three forms: plural (`operators`), singular (`operator`), and short name (`op`).
