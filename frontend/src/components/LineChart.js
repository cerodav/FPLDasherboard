import React, { Component } from "react";
import Highcharts from 'highcharts';
import HighchartsReact from 'highcharts-react-official';
import PropTypes from "prop-types";

class LineChart extends Component {
  render() {
    return (
        <HighchartsReact
          highcharts={Highcharts}
          options={this.props.options}
        />
    );
  }
}

LineChart.propTypes = {
  options: PropTypes.object.isRequired
};

export default LineChart;