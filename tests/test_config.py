import pytest

from mango import Tuner


def test_initial_custom():
    def objfun(params):
        return [param["a"] + param["b"] for param in params]

    param_space = {
        "a": range(1, 100),
        "b": range(1, 100),
    }
    x_init = [{"a": 1, "b": 1}, {"a": 2, "b": 2}]
    config = {"initial_custom": x_init}
    tuner = Tuner(param_space, objfun, conf_dict=config)
    results = tuner.run()

    x = results["params_tried"]
    # y = results["objective_values"]
    assert (x[: len(x_init)] == x_init).all()

    xy_init = [({"a": 1, "b": 1}, 2), ({"a": 2, "b": 2}, 4)]
    config = {"initial_custom": xy_init}
    tuner = Tuner(param_space, objfun, conf_dict=config)
    results = tuner.run()

    x = results["params_tried"]
    y = results["objective_values"]
    x_init = [xy[0] for xy in xy_init]
    y_init = [xy[1] for xy in xy_init]
    assert (x[: len(x_init)] == x_init).all()
    assert (y[: len(y_init)] == y_init).all()

    with pytest.raises(
        TypeError,
        match=r"Elements of initial_custom param should be either a dict of params or tuple",
    ):
        xy_init = {"a": 1, "b": 1}
        config = {"initial_custom": xy_init}
        tuner = Tuner(param_space, objfun, conf_dict=config)
        tuner.run()
