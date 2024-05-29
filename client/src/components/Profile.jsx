import { useCallback, useEffect, useState } from "react";
import Button from "react-bootstrap/Button";
import Form from "react-bootstrap/Form";
import { backendUrl } from "../utils/constants";
import { Navigate } from "react-router-dom";
import { useAuth } from "../contextProvider/AuthProvider";
import Container from "react-bootstrap/esm/Container";

const initialProfileData = { email: "", age: "", name: "" };
function Profile() {
  const [profileData, setProfileData] = useState(initialProfileData);

  const { token, resetAuthToken } = useAuth();

  const handleOnChange = (e) => {
    setProfileData({ ...profileData, [e.target.name]: e.target.value });
  };

  const fetchProfile = useCallback(async () => {
    try {
      const { email, age, name } = await fetch(`${backendUrl}/profile`, {
        headers: { Authorization: `Bearer ${token}` },
      }).then((res) => {
        console.log(res);
        if (res.ok) {
          return res.json();
        }
        if (res.status >= 400 && res.status <= 499) {
          resetAuthToken();
          throw new Error("token expired");
        } else throw new Error(res.statusText);
      });
      setProfileData({ email, age, name });
    } catch (error) {
      alert(`Error:${error.message}`);
    }
  }, [token, resetAuthToken]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await fetch(`${backendUrl}/profile`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({name:profileData.name,age:profileData.age}),
      });
      if (res.ok) alert("Profile updated successfully");
      else alert(`Error:${res.statusText}`);
    } catch (error) {
      alert(`Error:${error.message}`);
    }
  };

  useEffect(() => {
    if (token) fetchProfile();
  }, [token, fetchProfile]);

  if (!token) return <Navigate to="/login" />;

  return (
    <Container>
      <h1 style={{ textAlign: "center" }}>Profile</h1>
      <Form onSubmit={handleSubmit}>
        <Form.Group className="mb-3" controlId="formBasicEmail">
          <Form.Label>Email address</Form.Label>
          <Form.Control
            type="email"
            name="email"
            placeholder="Enter email"
            value={profileData.email}
            onChange={handleOnChange}
            disabled
          />
        </Form.Group>
        <Form.Group className="mb-3" controlId="formBasicName">
          <Form.Label>Name</Form.Label>
          <Form.Control
            type="text"
            name="name"
            placeholder="Enter name"
            value={profileData.name}
            onChange={handleOnChange}
          />
        </Form.Group>
        <Form.Group className="mb-3" controlId="formBasicAge">
          <Form.Label>Age</Form.Label>
          <Form.Control
            type="number"
            name="age"
            placeholder="Enter age"
            value={profileData.age}
            onChange={handleOnChange}
          />
        </Form.Group>
        <Button variant="primary" type="submit">
          Submit
        </Button>
      </Form>
    </Container>
  );
}

export default Profile;
