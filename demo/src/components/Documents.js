import React, { Component } from "react";
import Card from "@material-ui/core/Card";
import CardActions from "@material-ui/core/CardActions";
import CardContent from "@material-ui/core/CardContent";
import Button from "@material-ui/core/Button";
import Typography from "@material-ui/core/Typography";
import Grid from "@material-ui/core/Grid";

function Documents(props) {
  if (!Array.isArray(props.documents) || !props.documents.length) {
    return <Typography> Nothing to see here... </Typography>;
  }
  return props.documents.map(d => (
    <div>
      <br />
      <Doc key={d.id} document={d} />
    </div>
  ));
}

class Doc extends Component {
  render() {
    const doc = this.props.document;
    return (
      <Card style={{ textAlign: "left" }}>
        <CardContent>
          <Grid container direction="row" spacing={24}>
            <Grid item xs={4}>
              <DocHeader
                headline={doc.headline}
                entity={doc.entity}
                sentiment={doc.sentiment}
              />
            </Grid>
            <Grid item xs={8}>
              <Typography component="p">{doc.content}</Typography>
            </Grid>
          </Grid>
        </CardContent>
        <CardActions>
          <Button size="small" color="primary">
            More
          </Button>
        </CardActions>
      </Card>
    );
  }
}

function DocHeader(props) {
  return (
    <div>
      <Typography
        variant="h5"
        component="h2"
        style={{ whiteSpace: "normal", wordWrap: "break-word" }}
      >
        {props.headline}
      </Typography>
      <div style={{ display: "flex", justifyContent: "space-between" }}>
        <Typography color="textSecondary">
          Main Entity: {props.entity}
        </Typography>
        <Typography color="textSecondary">
          Sentiment: {props.sentiment}
        </Typography>
      </div>
    </div>
  );
}

export default Documents;
