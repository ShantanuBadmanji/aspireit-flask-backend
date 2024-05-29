import { useState } from "react";
import Button from "react-bootstrap/Button";
import Form from "react-bootstrap/Form";
import { backendUrl } from "../utils/constants";
import { Navigate } from "react-router-dom";
import { useAuth } from "../contextProvider/AuthProvider";
import Container from "react-bootstrap/esm/Container";

// eslint-disable-next-line react/prop-types
function UploadFile({ fetchUserFiles }) {
  const [upfile, setUpfile] = useState(null);
  const { token, resetAuthToken } = useAuth();

  const handleOnChange = (e) => setUpfile(e.target.files[0]);
  const handleSubmit = async (e) => {
    e.preventDefault();
    const formData = new FormData();
    formData.append("file", upfile);
    try {
      const res = await fetch(`${backendUrl}/uploads-mongodb`, {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`,
        },
        body: formData,
      });
      if (res.ok) {
        alert("File uploaded successfully");
        fetchUserFiles();
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
      <h1 style={{ textAlign: "center" }}>Upload Any File</h1>
      <Form onSubmit={handleSubmit}>
        <Form.Group controlId="formFile" className="mb-3">
          <Form.Label>Upload File</Form.Label>
          <Form.Control
            type="file"
            onChange={handleOnChange}
            name="file"
            required
          />
        </Form.Group>
        <Button variant="primary" type="submit">
          Submit
        </Button>
      </Form>
    </Container>
  );
}

export default UploadFile;
