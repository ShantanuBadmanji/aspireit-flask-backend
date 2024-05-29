import { useRef } from "react";
import Button from "react-bootstrap/Button";
import Form from "react-bootstrap/Form";
import { backendUrl } from "../utils/constants";
import { useAuth } from "../contextProvider/AuthProvider";
import { Navigate } from "react-router-dom";
import Container from "react-bootstrap/esm/Container";

function Login() {
  const { token, setAuthToken } = useAuth();
  const emailRef = useRef();
  const passwordRef = useRef();

  async function handleSubmit(e) {
    e.preventDefault();
    const email = emailRef.current.value;
    const password = passwordRef.current.value;
    // console.log(email, password);

    try {
      const { access_token: accessToken } = await fetch(`${backendUrl}/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
      }).then((res) => res.json());

      // console.log(accessToken);
      setAuthToken(accessToken);
    } catch (error) {
      alert(`Error:${error.message}`);
    }
  }

  if (token) return <Navigate to="/profile" />;

  return (
    <Container>
      <h1 style={{ textAlign: "center" }}>Login</h1>
      <Form onSubmit={handleSubmit}>
        <Form.Group className="mb-3" controlId="formBasicEmail">
          <Form.Label>Email address</Form.Label>
          <Form.Control type="email" placeholder="Enter email" ref={emailRef} />
          <Form.Text className="text-muted">
            Well never share your email with anyone else.
          </Form.Text>
        </Form.Group>

        <Form.Group className="mb-3" controlId="formBasicPassword">
          <Form.Label>Password</Form.Label>
          <Form.Control
            type="password"
            placeholder="Password"
            ref={passwordRef}
          />
        </Form.Group>
        <Button variant="primary" type="submit">
          Submit
        </Button>
      </Form>
    </Container>
  );
}

export default Login;
