import { navlinks } from "../utils/constants";
import Container from "react-bootstrap/Container";
import Nav from "react-bootstrap/Nav";
import Navbar from "react-bootstrap/Navbar";
import Button from "react-bootstrap/esm/Button";
import { NavLink } from "react-router-dom";
import { useAuth } from "../contextProvider/AuthProvider";

export default function MyNavbar() {
  const { token, resetAuthToken } = useAuth();
  return (
    <Navbar expand="lg" className="bg-body-tertiary d-flex">
      <Container>
        <Navbar.Brand href="/">MY App</Navbar.Brand>
        <Navbar.Toggle aria-controls="basic-navbar-nav" />
        <Navbar.Collapse id="basic-navbar-nav" className="d-flex">
          <Nav className="d-flex justify-content-between flex-grow-1 align-items-center">
            <div className="me-auto d-flex gap-2 flex-grow-1 mx-4 align-items-center">
              {navlinks.map(({ href, text }, i) => {
                return (
                  <NavLink key={i} to={href} className="">
                    {text}
                  </NavLink>
                );
              })}
            </div>
            {token && (
              <Button
                variant="danger"
                type="button"
                onClick={() => resetAuthToken()}
                className=""
              >
                Logout
              </Button>
            )}
          </Nav>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
}
