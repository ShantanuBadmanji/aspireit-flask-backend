import { useCallback, useEffect, useState } from "react";
import { backendUrl } from "../utils/constants";
import { Navigate } from "react-router-dom";
import { useAuth } from "../contextProvider/AuthProvider";
import UploadFile from "./UploadFile";
import Button from "react-bootstrap/esm/Button";
import Container from "react-bootstrap/esm/Container";

function File() {
  const { token, resetAuthToken } = useAuth();
  const [fileNames, setFileNames] = useState([]);
  // const [previewFileName, setPreviewFileName] = useState("");

  const fetchUserFiles = useCallback(async () => {
    try {
      const fNames = await fetch(`${backendUrl}/uploads-mongodb`, {
        headers: { Authorization: `Bearer ${token}` },
      }).then((res) => {
        if (res.ok) {
          return res.json();
        }
        if (res.status >= 400 && res.status <= 499) {
          resetAuthToken();
          throw new Error("token expired");
        } else throw new Error(res.statusText);
      });
      setFileNames([...fNames]);
    } catch (error) {
      alert(`Error:${error.message}`);
    }
  }, [token, resetAuthToken]);

  const handleOnClick = async (fileName) => {
    try {
      const res = await fetch(`${backendUrl}/uploads-mongodb/${fileName}`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      if (res.ok) {
        const blob = await res.blob();
        const url = URL.createObjectURL(blob);
        window.open(url);
      } else {
        alert(`Error:${res.statusText}`);
      }
    } catch (error) {
      alert(`Error:${error.message}`);
    }
  };

  useEffect(() => {
    if (token) fetchUserFiles();
  }, [token, fetchUserFiles]);

  if (!token) return <Navigate to="/login" />;

  return (
    <Container>
      <UploadFile fetchUserFiles={fetchUserFiles} />
      <div>
        <h2 style={{ textAlign: "center" }}>My Files</h2>
        <div className="d-flex flex-column w-50 sm:w-100 m-auto">
          {fileNames.map((fileName, i) => (
            <Button
              key={i}
              variant="outline-primary"
              type="button"
              onClick={() => handleOnClick(fileName)}
            >
              {fileName}
            </Button>
          ))}
        </div>
      </div>
      {/* <PreviewFile fileName={previewFileName} /> */}
    </Container>
  );
}

export default File;
