import React from 'react';

function Dropdown ({ selectedItem, data, handleChange }) {
    return (
        <React.Fragment>
            <div className="state-selection">
                <div className="dropdown">
                    <select value={selectedItem} onChange={handleChange}>
                    {
                        data.map((item) => {
                            return (
                                <option value={item.value} key={item.key} >
                                    {item.label}
                                </option>
                            );
                        })
                    }
                    </select>
                </div>
            </div>
        </React.Fragment>
    )
}

export default Dropdown;