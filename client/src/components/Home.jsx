import { useEffect, useState } from "react";
import Container from "react-bootstrap/esm/Container";

export default function Home() {
  const [homeData, setHomeData] = useState("");
  useEffect(() => {
    fetch("http://localhost:5000/")
      .then((res) => res.json())
      .then((data) => {
        console.log(data);
        setHomeData(data.message);
      });
  }, []);
  return (
    <Container>
      <h1 style={{ textAlign: "center" }}>Home</h1>
      <h2 style={{ textAlign: "center" }}> {homeData}</h2>
    </Container>
  );
}
