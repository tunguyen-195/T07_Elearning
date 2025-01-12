import React, { Component } from "react";
import { Input, Button } from "@material-ui/core";
import "./Home.css";

class Home extends Component {
  constructor(props) {
    super(props);
    this.state = {
      url: "",
    };
  }

  handleChange = (e) => this.setState({ url: e.target.value });

  join = () => {
    const { url } = this.state;
    if (url.trim() !== "") {
      const segments = url.split("/");
      window.location.href = `/${segments[segments.length - 1]}`;
    } else {
      const randomUrl = Math.random().toString(36).substring(2, 7);
      window.location.href = `/${randomUrl}`;
    }
  };

  navigateHome = () => {
    window.location.href = "http://127.0.0.1:5000/";
  };

  render() {
    return (
      <div className="home-container">
        <header className="home-header">
          <span className="home-title">Trang chủ</span>
          <img
            src="logo.png"
            alt="Logo"
            className="home-logo"
            onClick={this.navigateHome}
          />
        </header>

        <main className="home-main">
          <section className="home-intro">
            <h1 className="home-heading">Vào phòng học trực tuyến</h1>
            <p className="home-subtext">
              Phòng học trực tuyến của Khoa CNTT Trường Đại học Kỹ thuật - Hậu
              cần CAND
            </p>
          </section>

          <section className="home-panel">
            <p className="panel-title">Bắt đầu ngày hoặc tham gia phòng học</p>
            <Input
              placeholder="URL"
              value={this.state.url}
              onChange={this.handleChange}
              className="home-input"
              disableUnderline
            />
            <Button
              variant="contained"
              color="primary"
              onClick={this.join}
              className="home-button"
            >
              Go
            </Button>
          </section>
        </main>
      </div>
    );
  }
}

export default Home;
