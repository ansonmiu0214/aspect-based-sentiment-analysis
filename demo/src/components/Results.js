import React from "react";
import Typography from "@material-ui/core/Typography";
import Card from "@material-ui/core/Card";
import CardContent from "@material-ui/core/CardContent";

function Results(props) {
  const results = props.results;
  const scoreTitle = results.entity ? "Score: " : "";
  return (
    <div>
      <div style={{ display: "flex", justifyContent: "space-between" }}>
        <Typography variant="h3" gutterBottom>
          {results.entity}
          {results.attribute ? ` - ${results.attribute}` : ""}
        </Typography>
        <Typography variant="h3" gutterBottom>
          {scoreTitle}
          {results.entity ? (results.score ? results.score : "?") : ""}
        </Typography>
      </div>
      {results.entries.map(e => (
        <div key={e.attribute}>
          <Entry attribute={e.attribute} score={e.score} entries={e.entries} />
          <br />
        </div>
      ))}
    </div>
  );
}

function Entry(props) {
  return (
    <Card style={{ textAlign: "left" }}>
      <CardContent>
        <Typography variant="h5">{props.attribute}</Typography>
        <Typography>Score: {props.score}</Typography>
        {props.entries.map(e => (
          <Typography key={e.expression}>
            "{e.expression}
            ", ({e.sentiment}){" "}
          </Typography>
        ))}
      </CardContent>
    </Card>
  );
}

export default Results;
