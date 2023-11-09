from itertools import product
from jinja2 import Template
import yaml


_jinja_template_string = """You are {{name}}. Facts about yourself: {{socio_behavioral}}. Your goal: {{target}}. Facts about the apartment: {{apartment}}."""


def _load_yaml_data(subfolder: str, yaml_content: str):
    with open(
        f"../../assets/prompts/{subfolder}/{yaml_content}.yaml", "r", encoding="utf-8"
    ) as file:
        return yaml.safe_load(file)


def _load_landlord_config():
    return (
        _load_yaml_data("landlord", yaml_content)
        for yaml_content in [
            "name",
            "socio-behavioral",
            "target",
        ]
    )


def _load_renter_config():
    return (
        _load_yaml_data("renter", yaml_content)
        for yaml_content in ["name", "socio-behavioral", "target"]
    )


def _load_product_config():
    for item in _load_yaml_data("product", "apartment"):
        yield item


def all_landlord_variants():
    name, socio_behavioral, target = _load_landlord_config()
    apartment = _load_product_config()

    variants = product(name, socio_behavioral, target, apartment)

    return [
        (
            {
                "name_id": name["id"],
                "socio_behavioral_id": socio_behavioral["id"],
                "target_id": target["id"],
                "apartment_id": apartment["id"],
            },
            render_system_message(
                name["content"],
                socio_behavioral["content"],
                target["content"],
                apartment["content"],
            ),
        )
        for name, socio_behavioral, target, apartment in variants
    ]


def all_renter_variants():
    name, socio_behavioral, target = _load_renter_config()
    apartment = _load_product_config()

    variants = product(name, socio_behavioral, target, apartment)

    return [
        (
            {
                "name_id": name["id"],
                "socio_behavioral_id": socio_behavioral["id"],
                "target_id": target["id"],
                "apartment_id": apartment["id"],
            },
            render_system_message(
                name["content"],
                socio_behavioral["content"],
                target["content"],
                apartment["content"],
            ),
        )
        for name, socio_behavioral, target, apartment in variants
    ]


def all_variants():
    landlord_variants = all_landlord_variants()
    renter_variants = all_renter_variants()

    all_variants = product(landlord_variants, renter_variants)

    return [(variant) for variant in all_variants]


def render_system_message(
    name: str, socio_behavioral: str, target: str, apartment: str
) -> str:
    jinja_template = Template(_jinja_template_string)

    return jinja_template.render(
        name=name,
        socio_behavioral=socio_behavioral,
        target=target,
        apartment=apartment,
    )


# example all variants
all = all_variants()
print(len(all))  # get number of all variants
# print(all[0])  # get first variant of landlord and renter variant combination
# print(all[0][0])  # get first variant of landlord variants
print(all[0][0][1])  # get system message of first variant of landlord variants
