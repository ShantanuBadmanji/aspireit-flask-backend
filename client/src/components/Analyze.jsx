import { useState } from "react";
import Button from "react-bootstrap/Button";
import Form from "react-bootstrap/Form";
import { backendUrl } from "../utils/constants";
import { Navigate } from "react-router-dom";
import { useAuth } from "../contextProvider/AuthProvider";
import Container from "react-bootstrap/esm/Container";

// eslint-disable-next-line react/prop-types
function Analyze() {
  const { token, resetAuthToken } = useAuth();
  const [text, setText] = useState("");
  const [sentimentData, setSentimentData] = useState({ score: 0, label: "" });

  const handleOnChange = (e) => setText(e.target.value);

  const handleOnSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await fetch(`${backendUrl}/analyze`, {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ text }),
      });
      if (res.ok) {
        const { prediction } = await res.json();
        console.log(prediction[0]);
        setSentimentData({ ...prediction[0] });
      } else if (res.status == 401 || res.status == 403 || res.status == 422) {
        resetAuthToken();
      } else {
        const text = await res.text();
        alert(`Error:${text}`);
      }
    } catch (error) {
      alert(`Error:${error.message}`);
    }
  };

  if (!token) return <Navigate to="/login" />;
  return (
    <Container>
      <h1 style={{ textAlign: "center" }}>Analyze The Text</h1>
      <Form onSubmit={handleOnSubmit}>
        <Form.Group controlId="formFile" className="mb-3">
          <Form.Label>Enter Text</Form.Label>
          <Form.Control
            as="textarea"
            rows={3}
            onChange={handleOnChange}
            name="text"
            required
            value={text}
          />
        </Form.Group>
        <Button variant="primary" type="submit">
          Submit
        </Button>
      </Form>
      <div>
        <h2 style={{ textAlign: "center" }}>Sentiment Analysis</h2>
        <div className="d-flex flex-column w-50 sm:w-100 m-auto">
          <h3>Score: {sentimentData.score}</h3>
          <h3>Label: {sentimentData.label}</h3>
        </div>
      </div>
    </Container>
  );
}

export default Analyze;
