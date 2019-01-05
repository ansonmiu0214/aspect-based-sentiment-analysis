import React, { Component } from "react";
import TextField from "@material-ui/core/TextField";
import Button from "@material-ui/core/Button";
import CloudUploadIcon from "@material-ui/icons/CloudUpload";
import Divider from "@material-ui/core/Divider";
import Grid from "@material-ui/core/Grid";
import axios from "axios";

class ABSALoad extends Component {
  constructor(props) {
    super(props);
    this.fileInput = React.createRef();
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  handleSubmit(e) {
    e.preventDefault();
    if (!this.fileInput.current) {
      return;
    }

    let formData = new FormData();
    formData.append("file", this.fileInput.current.files[0]);
    axios
      .post("http://localhost:5000/absa/load", formData, {
        headers: {
          "Content-Type": "multipart/form-data"
        }
      })
      .catch(e => console.log(e));
  }

  render() {
    return (
      <Grid
        container
        direction="column"
        spacing={16}
        justify="center"
        alignItems="center"
      >
        <Grid item>
          <input
            accept=".xml, .txt"
            id="contained-button-file"
            multiple
            type="file"
            style={{ display: "none" }}
            ref={this.fileInput}
          />
          <label htmlFor="contained-button-file">
            <Button variant="contained" color="default" component="span">
              Upload
              <CloudUploadIcon style={{ marginLeft: "0.25em" }} />
            </Button>
          </label>
        </Grid>
        <Grid item>
          <Button
            variant="contained"
            color="default"
            component="span"
            onClick={this.handleSubmit}
          >
            Submit
          </Button>
        </Grid>
      </Grid>
    );
  }
}

class ABSAQuery extends Component {
  constructor(props) {
    super(props);
    this.state = {
      entity: "",
      attribute: ""
    };

    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
    this.handleKeyPress = this.handleKeyPress.bind(this);
  }

  handleChange = name => event => {
    this.setState({
      [name]: event.target.value
    });
  };

  handleSubmit(e) {
    e.preventDefault();
    const entity = this.state.entity;
    if (!entity) {
      return;
    }
    const attribute = this.state.attribute;

    this.props.setLoading(true)
    axios
      .get("/absa/query", {
        params: { entity, attribute }
      })
      .then(r => {
        this.props.setLoading(false)
        this.props.updateResults({ entity, attribute, ...r.data })
      })
      .catch(e => {
        this.props.setLoading(false)
        console.log(e)
      });
  }

  handleKeyPress(e) {
    if (e.key === "Enter") {
      this.handleSubmit(e);
    }
  }

  render() {
    return (
      <Grid
        container
        direction="column"
        spacing={16}
        justify="center"
        alignItems="center"
      >
        <Grid item>
          <TextField
            required
            label="Entity"
            value={this.state.entity}
            onChange={this.handleChange("entity")}
            onKeyPress={this.handleKeyPress}
          />
        </Grid>
        <Grid item>
          <TextField
            label="Attribute"
            value={this.state.attribute}
            onChange={this.handleChange("attribute")}
            onKeyPress={this.handleKeyPress}
          />
        </Grid>
        <Grid item>
          <Button
            variant="contained"
            color="default"
            component="span"
            onClick={this.handleSubmit}
          >
            Submit
          </Button>
        </Grid>
      </Grid>
    );
  }
}

class Options extends Component {
  render() {
    return (
      <ABSAQuery setLoading={this.props.setLoading} updateResults={this.props.updateResults} />
      // <div>
      //   <ABSALoad />
      //   <br />
      //   <Divider />
      //   <br />
      //   <ABSAQuery updateResults={this.props.updateResults} />
      // </div>
    );
  }
}

export default Options;
