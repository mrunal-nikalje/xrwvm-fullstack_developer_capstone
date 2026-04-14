import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import "./Dealers.css";
import "../assets/style.css";
import Header from '../Header/Header';

const PostReview = () => {
  const [dealer, setDealer] = useState({});
  const [review, setReview] = useState("");
  const [model, setModel] = useState("");
  const [year, setYear] = useState("");
  const [date, setDate] = useState("");
  const [carmodels, setCarmodels] = useState([]);

  let curr_url = window.location.href;
  let root_url = curr_url.substring(0, curr_url.indexOf("postreview"));

  let params = useParams();
  let id = params.id;

  // ✅ FIXED URLS (IMPORTANT)
  let dealer_url = root_url + `djangoapp/dealer/${id}`;
  let review_url = root_url + `djangoapp/add_review/`;   // <-- FIXED (added /)
  let carmodels_url = root_url + `djangoapp/get_cars`;

  // ===========================
  // POST REVIEW FUNCTION
  // ===========================
  const postreview = async () => {
    let name = sessionStorage.getItem("firstname") + " " + sessionStorage.getItem("lastname");

    // fallback if name is null
    if (name.includes("null")) {
      name = sessionStorage.getItem("username");
    }

    // validation
    if (!model || review === "" || date === "" || year === "") {
      alert("All details are mandatory");
      return;
    }

    // safer split
    let [make_chosen, model_chosen] = model.split(" ");

    let jsoninput = JSON.stringify({
      "name": name,
      "dealership": id,
      "review": review,
      "purchase": true,
      "purchase_date": date,
      "car_make": make_chosen,
      "car_model": model_chosen,
      "car_year": year,
    });

    console.log("Sending:", jsoninput);

    try {
      const res = await fetch(review_url, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: jsoninput,
      });

      const json = await res.json();
      console.log("Response:", json);

      if (json.status === 200) {
        window.location.href = window.location.origin + "/dealer/" + id;
      } else {
        alert("Error submitting review");
      }

    } catch (error) {
      console.error("Error:", error);
      alert("Server error while posting review");
    }
  };

  // ===========================
  // GET DEALER DETAILS
  // ===========================
  const get_dealer = async () => {
    const res = await fetch(dealer_url);
    const retobj = await res.json();

    if (retobj.status === 200) {
      let dealerobjs = Array.from(retobj.dealer);
      if (dealerobjs.length > 0)
        setDealer(dealerobjs[0]);
    }
  };

  // ===========================
  // GET CAR MODELS
  // ===========================
  const get_cars = async () => {
    const res = await fetch(carmodels_url);
    const retobj = await res.json();

    let carmodelsarr = Array.from(retobj.CarModels);
    setCarmodels(carmodelsarr);
  };

  useEffect(() => {
    get_dealer();
    get_cars();
  }, []);

  // ===========================
  // UI
  // ===========================
  return (
    <div>
      <Header />

      <div style={{ margin: "5%" }}>
        <h1 style={{ color: "darkblue" }}>{dealer.full_name}</h1>

        <textarea
          cols='50'
          rows='7'
          placeholder="Write your review..."
          onChange={(e) => setReview(e.target.value)}
        ></textarea>

        <div className='input_field'>
          Purchase Date
          <input type="date" onChange={(e) => setDate(e.target.value)} />
        </div>

        <div className='input_field'>
          Car Make & Model
          <select onChange={(e) => setModel(e.target.value)}>
            <option value="" disabled selected>Choose Car Make and Model</option>
            {carmodels.map((carmodel, index) => (
              <option key={index} value={carmodel.CarMake + " " + carmodel.CarModel}>
                {carmodel.CarMake} {carmodel.CarModel}
              </option>
            ))}
          </select>
        </div>

        <div className='input_field'>
          Car Year
          <input type="number" onChange={(e) => setYear(e.target.value)} min={2015} max={2023} />
        </div>

        <div>
          <button className='postreview' onClick={postreview}>
            Post Review
          </button>
        </div>

      </div>
    </div>
  );
};

export default PostReview;