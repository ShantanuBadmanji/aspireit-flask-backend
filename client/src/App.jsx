import { Outlet, Route, Routes } from "react-router-dom";
import MyNavbar from "./components/MyNavbar";
import Login from "./components/Login";
import Register from "./components/Register";
import Profile from "./components/Profile";
import Home from "./components/Home";
import File from "./components/File";
import Analyze from "./components/Analyze";

function Page() {
  return (
    <>
      <MyNavbar />
      <Outlet />
    </>
  );
}
function App() {
  return (
    <>
      <Routes>
        <Route path="/" element={<Page />}>
          <Route index element={<Home />} />
          <Route path="profile" element={<Profile />} />
          <Route path="login" element={<Login />} />
          <Route path="register" element={<Register />} />
          <Route path="file" element={<File />} />
          <Route path="analyze" element={<Analyze />} />
        </Route>
      </Routes>
    </>
  );
}
export default App;
