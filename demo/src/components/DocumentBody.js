import React from 'react';
import { Typography } from "@material-ui/core";

function DocumentBody(props) {
  const { id, components, metadata } = props.document
  const { date, headline, title } = metadata

  return (
    <div style={{marginBottom: '24px'}}>
      <Typography color="textSecondary" gutterBottom>
        Document #{id}
      </Typography>
      <Typography color="textSecondary" gutterBottom>
        {date}
      </Typography>
      <Typography color="textSecondary" gutterBottom>
        {title}
      </Typography>
      <Typography color="textSecondary" gutterBottom>
        {headline}
      </Typography>
      {
        components.map(({ text }, idx) => 
          <Typography key={idx} component="p" style={{marginBottom: '5px', lineHeight: '1.5rem'}}>{text}</Typography>
        )
      }
    </div>
  )
}

export default DocumentBody